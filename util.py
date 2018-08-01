import db

import os
import random
import configparser

from mutagen.easyid3 import EasyID3

parser = configparser.ConfigParser()
parser.read('config.ini')


def populate_song_db():
	path = parser.get('music', 'music_dir')
	files = filter(lambda x: x.endswith('.mp3'), os.listdir(path))
	songs = []

	for f in files:
		try:
			filename = os.path.abspath(path + f)

			song_file = EasyID3(filename)

			artist = song_file.get("artist")[0]
			album = song_file.get("album")[0]
			title = song_file.get("title")[0]

			song = db.Song(f, artist, album, title)
			
		except TypeError as e:
			song = db.Song(f, "TypeError", "TypeError", "TypeError")
		
		finally:
			db.Song.insert(song)


def is_mobile(ua):
	return ("Android" in ua) or ("iPhone" in ua) or ("Windows Phone" in ua)
