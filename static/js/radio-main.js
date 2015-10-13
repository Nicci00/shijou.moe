var OGG = "http://shijou.moe:8000/imas-radio.ogg";
var MP3 = "http://shijou.moe:8000/imas-radio-lq.mp3";
var radio = document.getElementById('radio-player');

function changeSource(src) {
  radio.src = src;
  radio.play();
}

function hideIRC(){
  var irc = ;
  document.getElementById("irc-div").remove(irc);
}
