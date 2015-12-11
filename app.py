#-*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request

from mutagen.easyid3 import EasyID3

import random
import sys
import os

from ConfigParser import SafeConfigParser

app = Flask(__name__)

parser = SafeConfigParser()
parser.read('config.ini')

app.config['music_path'] = parser.get('music', 'music_dir')

list_of_idols = None
list_of_songs = None


# MAIN PAGES
@app.route('/')
def root():
	return render_template('index.html')

@app.route('/imas-radio')
def radio():
	return render_template('imas-radio.html',
		noirc = request.args.has_key('noirc'),
		muted = request.args.has_key('muted'),
		ws_url= parser.get("app","ws_url"),
		oneyear = parser.getboolean('app','oneyear'))

@app.route('/imas-radio/song-list')
def song_list():
	return render_template('song-list.html', songs = list_of_songs)

@app.route('/imas-radio/info')
def radio_info():
	return render_template('imas-radio-info.html',
		ws_url = parser.get("app","ws_url"))

@app.route('/do-it-for-her')
def do_it_for_her():
	return render_template('do-it-for-her.html')

# UTILITIES
@app.route('/util-random-idol')
def random_idol():
	random_idol = random.choice(list_of_idols)
	return redirect('/static/img/idol-bg/' + random_idol)

@app.route('/its-happening')
def happening():
	return "It finally happened."

# REDIRECTS
@app.route('/imas-radio.html')
def radio_html_redirect():
	return redirect('/imas-radio', 301)

@app.route('/list-of-songs2.html')
def redirect_list():
	return redirect('/song-list', 301)

# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error/404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('error/500.html'),500

def list_song():
	files = os.listdir(app.config['music_path'])
	songs = []

	for f in files:
		try:
			song_file = EasyID3(app.config['music_path'] + f)
			song_title = song_file.get("title")[0]
			song_artist= song_file.get("artist")[0]
			songs.append([song_title, song_artist])

		except TypeError as e:
			songs.append([f, ''])

	return songs

if __name__ == '__main__':
	list_of_idols = os.listdir('static/img/idol-bg')
	list_of_songs = list_song()

	app.run(debug=parser.getboolean('app','debug'), host='0.0.0.0')
