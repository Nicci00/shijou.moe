import sqlite3
import configparser
import datetime

parser = configparser.ConfigParser()
parser.read('config.ini')

db = parser.get('db','dbfile')

##TODO better update (3)
##FINAL 05/12/18

class SideImage():
	def __init__(self, filename, source, id=0):
		self.filename = filename
		self.source = source
		self.id = id


	def __repr__(self):
		return ("<SideImage {} - {} - S? {}>".format(self.id, self.filename, bool(self.source)))


	def select_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from sideimage where id = ?", (id,))

		r = c.fetchall()
		conn.close()

		if (len(r) == 0):
			return None
		else:
			return SideImage(r[0][1], r[0][2], r[0][0])


	def select_filename(filename):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from sideimage where filename = ?", (filename,))

		r = c.fetchall()
		conn.close()

		if (len(r) == 0):
			return None
		else:
			return SideImage(r[0][1], r[0][2], r[0][0])


	def select_all():
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from sideimage")

		r = c.fetchall()
		conn.close()

		return list(map(lambda x: SideImage(x[1], x[2], x[0]), r))


	def insert(filename, source):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("insert into sideimage(filename, source) values (?,?)", (filename, source,))

		conn.commit()
		conn.close()


	def delete_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("delete from sideimage where id=?", (id,))

		conn.commit()
		conn.close()


	def update(id, src):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("update sideimage set source=? where id=?", (src, id))
		conn.commit()
		conn.close()


class Song():
	def __init__(self, filename, artist, album, title, id=0):
		self.filename = filename
		self.artist = artist
		self.album = album 
		self.title = title 
		self.id = id


	def __repr__(self):
		return ("<Song {} - {}>".format(self.id, self.filename))


	def select_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from song where id = ?", (id,))

		r = c.fetchall()
		conn.close()

		if (len(r) == 0):
			return None
		else:
			return Song(r[0][1], r[0][2], r[0][3], r[0][4], r[0][0])

	def select_filename(filename):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from song where filename = ?", (filename,))

		r = c.fetchall()
		conn.close()

		if (len(r) == 0):
			return None
		else:
			return Song(r[0][1], r[0][2], r[0][3], r[0][4], r[0][0])


	def select_all():
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from song")

		r = c.fetchall()
		conn.close()

		return list(map(lambda x: Song(x[1], x[2], x[3], x[4], x[0]), r))


	def insert(song, skip=False):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		if skip:
			query = "insert into song(filename, artist, album, title) values (?,?,?,?) on conflict do nothing"
		else:
			query = "insert into song(filename, artist, album, title) values (?,?,?,?)"

		c.execute(query, (song.filename, song.artist, song.album, song.title))

		conn.commit()
		conn.close()


	def delete_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("delete from song where id=?", (id,))

		conn.commit()
		conn.close()


	def update_id(song, id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("update song set filename=?, artist=?, album=?, title=? where id=?", 
			(song.filename, song.artist, song.album, song.title, id))
		conn.commit()
		conn.close()


class Newspost():
	def __init__(self, author, newstext, creationdate, id=0):
		self.id = id
		self.author = author
		self.newstext = newstext
		self.creationdate = creationdate


	def __repr__(self):
		return ("<Newspost {} - {}>".format(self.id, self.author))


	def select_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from newspost where id = ?", (id,))

		r = c.fetchall()
		conn.close()

		if (len(r) == 0):
			return None
		else:
			return Newspost(r[0][1], r[0][2], r[0][3][:-7], r[0][0])


	def select_all():
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from newspost")

		r = c.fetchall()
		conn.close()

		return list(map(lambda x: Newspost(x[1], x[2], x[3][:-7], x[0]), r))


	def select_all_desc():
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("select * from newspost order by id desc")

		r = c.fetchall()
		conn.close()

		return list(map(lambda x: Newspost(x[1], x[2], x[3][:-7], x[0]), r))


	def insert(newspost, skip=False):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		if skip:
			query = "insert into newspost(author, newstext, creationdate) values (?,?,?) on conflict do nothing"
		else:
			query = "insert into newspost(author, newstext, creationdate) values (?,?,?)"

		c.execute(query, (newspost.author, newspost.newstext, newspost.creationdate))

		conn.commit()
		conn.close()


	def delete_id(id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("delete from newspost where id=?", (id,))

		conn.commit()
		conn.close()


	def update_id(newspost, id):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("update newspost set author=?, newstext=?, creationdate=? where id=?", 
			(newspost.author, newspost.newstext, newspost.creationdate, id))
		conn.commit()
		conn.close()

