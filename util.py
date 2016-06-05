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
			filename = os.path.abspath(path + f)

			song_file = EasyID3(filename)
			song_title = song_file.get("title")[0]
			song_artist= song_file.get("artist")[0]
			songs.append(Song(filename.decode('utf-8'), song_title, song_artist))

		except TypeError as e:
			songs.append(Song(filename.decode('utf-8'), 'TypeError', 'TypeError'))

	return songs


class Song(object):
	def __init__(self, filename, title, artist):
		self.filename = filename
		self.title = title
		self.artist = artist


def is_mobile(ua):
	return ("Android" in ua) or ("iPhone" in ua) or ("Windows Phone" in ua)
