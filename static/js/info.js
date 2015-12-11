
function timestamp(){
	return "[" + String(Math.floor(Date.now() / 1000)) + "] ";
}

var ws = new WebSocket(socket_url);

ws.onopen = function(){
	console.log(timestamp() + "Connected alright")
}

ws.onmessage = function(event) {
	console.log(timestamp() + "Got data from server alright");
	var data = JSON.parse(event.data)
	document.getElementById("art").innerHTML = data.artist;
	document.getElementById("tit").innerHTML = data.title;
	document.getElementById("lis").innerHTML = data.listeners;
};

ws.onclose = function(event){
	console.log(timestamp() + "y tho")
}