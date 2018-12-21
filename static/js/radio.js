function ready(fn) {
  if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}

document.querySelector("#mp3-btn").addEventListener("click", function(){
    radio.src = "http://shijou.moe:8000/imas-radio-lq.mp3";
    radio.play();
    console.log(timestamp() + "Now using mp3 source");
});

document.querySelector("#ogg-btn").addEventListener("click", function(){
    radio.src = "http://shijou.moe:8000/imas-radio.ogg";
    radio.play();
    console.log(timestamp() + "Now using ogg-vorbis source");
});

function ws_init(url){
    var ws = new WebSocket(url);

    function timestamp(){
        return "[" + String(Math.floor(Date.now() / 1000)) + "] "
    }

    ws.onopen = function(){
        console.log(timestamp() + "Connected on " + url);
    };

    ws.onmessage = function(event) {
        console.log(timestamp() + "Got data");
        var data = JSON.parse(event.data);

        document.getElementById("art").innerHTML = data.artist;
        document.getElementById("tit").innerHTML = data.title;
        document.getElementById("lis").innerHTML = data.listeners;

        document.title = String(data.artist + " - " + data.title);
    };

    ws.onclose = function(event){
        console.log(timestamp() + "Disconnected");
    };
}

function change_image(){
    var image_source_link = document.querySelector("#image-source-link");
    var idol_image = document.querySelector("#side-image");
    var spinner = document.querySelector('#spinner');

    idol_image.style.visibility = 'hidden';

    spinner.className = 'fa fa-circle-o-notch fa-spin';
    spinner.style.visibility = '';

    var req = new XMLHttpRequest();
    req.open('GET', '/imas-radio/json/side_image', true);

    req.onload = function() {

        if (this.status >= 200 && this.status < 400) {
            var data = JSON.parse(this.responseText);

            idol_image.setAttribute('src', data.filename);
            image_source_link.href = data.source;

            spinner.className = '';
            spinner.style.visibility = 'hidden';

            idol_image.style.visibility = ''; 
        }
    };
    req.send();
}

ready(function() {
    var radio = document.getElementById('radio-player');
    radio.volume = 0.7;
    radio.style.visibility = "hidden";

    document.querySelector("#side-image").addEventListener("click", change_image);

    ws_init(ws_url);
});
