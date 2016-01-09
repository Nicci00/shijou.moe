import os
import random

from ConfigParser import SafeConfigParser
from mutagen.easyid3 import EasyID3

parser = SafeConfigParser()
parser.read('config.ini')


def listsongs():
	path = parser.get('music', 'music_dir')
	files = os.listdir(path)
	songs = []

	for f in files:
		try:
			song_file = EasyID3(path + f)
			song_title = song_file.get("title")[0]
			song_artist= song_file.get("artist")[0]
			songs.append([song_title, song_artist, f])

		except TypeError as e:
			songs.append([f, ''])

	return songs
