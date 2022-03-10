function do_ajax() {
    var req = new XMLHttpRequest();
    var result = document.getElementById('result');
    req.onreadystatechange = function()
    {
      const button = document.querySelector("button")
      if(this.readyState == 4 && this.status == 200) {
        button.disabled = false;
        result.innerHTML = this.responseText;
      } else {
        button.disabled = true;
        result.innerHTML = "処理中...";
      }
    }
    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("text=" + document.querySelector("#textarea").value);
    }