var radio = document.getElementById('radio-player');
var idol_image = document.querySelector("#side-image");
var ws = new WebSocket(socket_url);

radio.volume = 0.7;

radio.style.visibility = "hidden";

function timestamp(){
	return "[" + String(Math.floor(Date.now() / 1000)) + "] ";
}

ws.onopen = function(){
	console.log(timestamp() + "Connected alright")
}

ws.onmessage = function(event) {
	console.log(timestamp() + "Got data from server alright");
	var data = JSON.parse(event.data)

	document.getElementById("art").innerHTML = data.artist;
	document.getElementById("tit").innerHTML = data.title;
	document.getElementById("lis").innerHTML = data.listeners;

	document.title = String(data.artist + " - " + data.title)
};

ws.onclose = function(event){
	console.log(timestamp() + "y tho")
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


idol_image.addEventListener("click", function(){
	var req = new XMLHttpRequest();
	req.open('GET', '/imas-radio/util/side-image/?base64', true);

	req.onload = function() {
		if (this.status >= 200 && this.status < 400) {
			idol_image.src = String(this.response);
		}
	}
	req.send();
});


