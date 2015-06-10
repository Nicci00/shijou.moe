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

# MAIN PAGES
@app.route('/')
def root():
	return render_template('index.html')

@app.route('/imas-radio')
def radio():

   	return render_template('imas-radio.html', muted = request.args.has_key('muted'))

@app.route('/imas-radio/song-list')
def song_list():
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
	
	return render_template('song-list.html', songs = songs)

@app.route('/do-it-for-her')
def do_it_for_her():
	return render_template('do-it-for-her.html')

# UTILITIES
@app.route('/util-random-idol')
def random_idol():
	random_idol = random.choice(os.listdir('static/img/idol-bg')) 
	return redirect('/static/img/idol-bg/' + random_idol)

@app.route('/its-happening')
def happening():
	return render_template('its-happening.html')
		
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
		