from flask import Flask, redirect, render_template, request, make_response,\
	session, abort, send_from_directory, flash

from werkzeug.utils import secure_filename
from functools import wraps
import random
import configparser
import base64
import os

import util
import db

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read('config.ini')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = parser.get('app', 'secret_key')

# TODO
# Finish side image handling
# Shekel makings
# Donations
# ws info reliability
# News
# song popcon
# Multiple streams
# stats


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error/404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('error/500.html',
		admin_email = parser.get("contact", "admin_email")),500


# INTERNAL UTILITIES
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in set(['jpeg','jpg','png'])


@app.before_first_request
def appsetup():
	pass


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			logged = session['logged']
		except KeyError:
			abort(403)
		return f(*args, **kwargs)

	return decorated_function


# MAIN PAGES
@app.route('/')
def root():
	return render_template('index.html')


@app.route('/imas-radio/')
def radio():
	ws_url = "ws://{}:{}".format(
		parser.get('websockets', 'host'),
		parser.get('websockets', 'port')
		)

	return render_template('/radio/imas-radio.html',
		mobile = util.is_mobile(request.headers.get('User-Agent')),
		ws_url = ws_url)


@app.route('/imas-radio/song-list/')
def songlist():
	return render_template('radio/song-list.html',
		songs = db.Song.select_all())


@app.route('/imas-radio/donate/')
def donate():
	return render_template("/radio/donate.html")


@app.route('/imas-radio/help/')
def help():
	return render_template("/radio/help.html",
		email = parser.get("contact", "admin_email"))


@app.route('/do-it-for-her/')
def do_it_for_her():
	return render_template('do-it-for-her.html')

# ADMIN INTERFACE
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
	if request.method == 'POST':
		b_user = request.form['user'] == parser.get('admin', 'user')
		b_pass = request.form['pass'] == parser.get('admin', 'pass')

		if b_user and b_pass:
			session['logged'] = True
			return redirect('/admin/landing')
		else:
			abort(403)
	else:
		return render_template('radio/admin/login.html')


@app.route('/admin/landing', methods=['GET'])
@login_required
def admin_page():

	return render_template('radio/admin/admin.html')


@app.route('/admin/side-image-manager/')
@login_required
def side_image_manager():

	return render_template("radio/admin/side-image-mgr.html", 
		images = db.SideImage.select_all())


@app.route('/admin/song-data-manager/')
@login_required
def song_data_manager():

	return render_template("radio/admin/song-data-mgr.html",
		songs = db.Song.select_all())


@app.route('/admin/play-file/<path:file>')
@login_required
def play_file(file):
	folder = parser.get('music', 'music_dir')
	file = secure_filename(file)
	return send_from_directory(folder, file)


@app.route('/admin/logout')
def admin_logout():
	try:
		if session['logged']:
			session.pop('logged', None)
			return redirect('/')
	except KeyError:
		return "Not logged"

#FORM ENDPOINTS
@app.route('/admin/song-data-manager/update_song', methods=['POST'])
@login_required
def update_song_data():
	id = request.form['song_id']

	filename = request.form['song_filename']
	new_artist = request.form['song_artist']
	new_title = request.form['song_title']
	new_album = request.form['song_album']

	s = db.Song(filename, new_artist, new_album, new_title)

	db.Song.update_id(s, id)

	return redirect('/admin/song-data-manager')


@app.route('/admin/side-image-manager/update_image', methods=['POST'])
@login_required
def update_image_data():
	id = request.form['image_id']
	source = request.form['image_source']

	db.SideImage.update(id, source)

	return redirect('/admin/side-image-manager')


@app.route('/admin/side-image-manager/upload_image', methods=['POST'])
@login_required
def upload_image():
	if "image" in request.files and request.files['image'].filename != "":

		file = request.files['image']
		filename = secure_filename(file.filename)
		folderpath = 'static/img/side_images'

		file.save(os.path.join(folderpath, filename))

		if "source" in request.form:
			print(filename)
			db.SideImage.insert(filename, request.form["source"])
		else:
			db.SideImage.insert(filename, None)
	else:
		return "javascript:alert('malformed request')"

	return redirect("/admin/side-image-manager/")


@app.route('/admin/side-image-manager/delete_image', methods=['POST'])
@login_required
def delete_image():

	if "image_id" in request.form and 'image_filename' in request.form:

		db.SideImage.delete_id(request.form['image_id'])

		imgpath = os.path.abspath('static/img/side_images/' + str(request.form['image_filename']))
		os.remove(imgpath)

	else:
		return "javascript:alert('malformed request')"

	return redirect("/admin/side-image-manager")

# UTILITIES
@app.route('/imas-radio/util/side-image/')
def random_idol():
	bg_path = 'static/img/side_images/'

	images = [i.filename for i in db.SideImage.select_all()]

	#this means its the users first image request
	if not 'images' in session.keys() and not 'index' in session.keys():
		session['index'] = 0
		session['images'] = random.sample(images,len(images))
	#user requested new image
	else:
		if session['index'] != len(session['images']) - 1:
			session['index'] = session['index'] + 1
		else:
			session['index'] = 0

	image_to_serve = bg_path + session['images'][session['index']]

	if 'path' in request.args:
			return "/" + image_to_serve
	else:
		response = make_response(redirect(image_to_serve))
		response.headers['Cache-Control'] = 'max-age=0'

	return response


if __name__ == '__main__':
	app.run()
