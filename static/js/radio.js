var radio = document.getElementById('radio-player');
radio.volume = 0.7;
radio.style.visibility = "hidden";

var idol_image = document.querySelector("#side-image");
idol_image.addEventListener("click", function(){

    var spinner = document.querySelector('#spinner');
    var current_src = idol_image.src


    idol_image.style.visibility = 'hidden';

    spinner.className = 'fa fa-circle-o-notch fa-spin';
    spinner.style.visibility = '';

    var req = new XMLHttpRequest();
    req.open('GET', '/imas-radio/util/side-image/?path', true);

    req.onload = function() {

        if (this.status >= 200 && this.status < 400) {
            idol_image.setAttribute('src', this.responseText);
        }

        idol_image.style.visibility = ''; 

        spinner.className = '';
        spinner.style.visibility = 'hidden';
    };

    req.send();
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

ws_init(ws_url);