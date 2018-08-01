import sqlite3

db = 'shijoumoe.db'

##TODO better update (3)
##FINAL 10/07/18

class SideImage():

	def __init__(self, filename, source, id=None):
		self.filename = filename
		self.source = source
		
		if id is None:
			self.id = 0
		else:
			self.id = id


	def __repr__(self):
		return ("<SideImage id:{} - {}".format(self.id, self.filename))


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
	def __init__(self, filename, artist, album, title, id=None):
		self.filename = filename
		self.artist = artist
		self.album = album 
		self.title = title 

		if id is None:
			self.id = 0
		else:
			self.id = id


	def __repr__(self):
		return ("<Song id:{} - {}".format(self.id, self.filename))


	def select_id():
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


	def insert(song):
		global db

		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("insert into song(filename, artist, album, title) values (?,?,?,?)",
			(song.filename, song.artist, song.album, song.title))

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