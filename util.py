import db

import os
import random
import configparser

from mutagen.easyid3 import EasyID3

parser = configparser.ConfigParser()
parser.read('config.ini')

def populate_song_db():
	path = parser.get('music', 'music_dir')
	files = list(filter(lambda x: x.endswith('.mp3'), os.listdir(path)))

	if not files:
		raise Exception("No files to populate DB with")
	else:
		print("Populating DB with {} files".format(len(files)) )

	songs = []
	error = False

	for f in files:
		try:
			print("Extracting data from " + f)
			filename = os.path.abspath(path + f)

			song_file = EasyID3(filename)

			artist = song_file.get("artist")[0]
			album = song_file.get("album")[0]
			title = song_file.get("title")[0]

			songs.append(db.Song(f, artist, album, title))
			
		except Exception as e:
			print("Exception processing file " + f)
			print(str(e) + "\n")
			error = True
			break

	if not error:
		[db.Song.insert(s, skip = True) for s in songs]


def is_mobile(ua):
	return ("Android" in ua) or ("iPhone" in ua) or ("Windows Phone" in ua)

def token_validate(token):
	pass

def token_create(expiration_date):
	pass

if __name__ == '__main__':
	populate_song_db()