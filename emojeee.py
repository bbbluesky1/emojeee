from flask import *
import numpy as np
import pickle
import MeCab
import csv
import pandas as pd

app = Flask(__name__)

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        tagger = MeCab.Tagger("-Owakati")
        words = tagger.parse(request.form["text"]).split()
        with open('./static/word2vec_model.pkl', mode='rb') as fp:
            model = pickle.load(fp)
        word_vecs = []
        for word in words:
            try:
                word_vecs.append(model[word])
            except:
                pass
        v = np.asarray(word_vecs)
        query_vector = np.nanmean(v,axis=0)
        cos_list = []
        num = 0
        with open('./static/doc_vector.pkl', mode='rb') as fp:
            doc_vectors = pickle.load(fp)
        for doc_vector in doc_vectors:
            cos_result = cos_sim(query_vector,doc_vector)
            if cos_result.dtype != 'float64':
                cos_list.append([cos_result,num])
                num += 1
        df = pd.read_csv('./static/Tweetsdata2.csv', encoding='utf-8')
        index = max(cos_list, key=lambda x:x[0])[1]
        return request.form['text']+df.iat[index,1]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
