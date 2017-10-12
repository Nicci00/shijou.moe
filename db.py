import sqlite3
db = 'shijoumoe.db'

class SideImage(object):
	def __init__(self, id, filename, src):
		self.id = id
		self.filename = filename
		self.src = src 

def init_db():
	global db

	try:
		conn = sqlite3.connect(db)
		c = conn.cursor()
	
		c.executescript("""
			create table side_image (
				id integer primary key autoincrement,
				filename varchar2 unique,
				src varchar2
		);""")

		conn.close()
	except (sqlite3.DatabaseError, sqlite3.Error) as e:
		print("Error in init_db: " + e.stacktrace)


def select_id(id):
	global db

	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("select * from side_image where id = ?", (id,))

	r =c.fetchall()
	conn.close()

	return list(map(lambda x: SideImage(x[0], x[1], x[2]), r))[0]


def select_all():
	global db

	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("select * from side_image")

	r =c.fetchall()
	conn.close()

	return list(map(lambda x: SideImage(x[0], x[1], x[2]), r))


def insert(filename, src):
	global db

	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("insert into side_image(filename, src) values (?,?)", (filename, src,))

	conn.commit()
	conn.close()


def delete_id(id):
	global db

	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("delete from side_image where id=?", (id,))

	conn.commit()
	conn.close()


def update_id(filename, src, id):
	global db

	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("update side_image set filename=?, src=? where id=?", (filename, src, id))
	conn.commit()
	conn.close()


