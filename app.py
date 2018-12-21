from flask import Flask, redirect, render_template, request, make_response,\
	session, abort, send_from_directory, flash, jsonify, url_for

from werkzeug.utils import secure_filename
from functools import wraps
import random
import configparser
import base64
import os
import sys
import json
import datetime

import util
import db

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read('config.ini')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = parser.get('app', 'secret_key')

# TODO
# Finish side image handling (add source information) (DONE)
# Dark theme (wip)
# Shekel makings(done?)
# Donations (done)
# WS info reliability
# News (wip)
# Song popcon
# Multiple streams
# Stats
# message board

# ERROR HANDLERS
@app.errorhandler(404)
def e_page_not_found(e):
	return render_template('error/404.html'),404


@app.errorhandler(500)
def e_internal_server_error(e):
	return render_template('error/500.html',
		admin_email = parser.get("contact", "admin_email")),500


# INTERNAL UTILITIES
def preprocess_sideimages():
	images = db.SideImage.select_all()
	rl = []

	for i in images:

		if i.source is None:
			i.source = url_for('v_nosauce', filename = i.filename)

		i.filename = url_for('static', \
			filename='img/side_images/'+i.filename, _external = True)

		rl.append(i.__dict__)

	return rl


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in set(['jpeg','jpg','png'])


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
def v_root():
	return render_template('index.html')


@app.route('/imas-radio/')
def v_radio():

	if not 'images' in session and not 'index' in session:
		images = preprocess_sideimages()
		random.shuffle(images)

		session['images'] = images
		session['index'] = 0


	ws_url = "ws://{}:{}".format(parser.get('websockets', 'host'),
		parser.get('websockets', 'port'))

	side_image = session['images'].__getitem__(session['index'])

	return render_template('/radio/imas-radio.html',
		mobile = util.is_mobile(request.headers.get('User-Agent')),
		side_image = side_image,
		ws_url = ws_url)


@app.route('/imas-radio/song-list/')
def v_songlist():
	return render_template('radio/song-list.html',
		songs = db.Song.select_all())


@app.route('/imas-radio/donate/')
def v_donate():
	return render_template("/radio/donate.html")


@app.route('/imas-radio/help/')
def v_help():
	return render_template("/radio/help.html",
		email = parser.get("contact", "admin_email"))


@app.route('/do-it-for-her/')
def v_doitforher():
	return render_template('do-it-for-her.html')


@app.route('/imas-radio/news/')
def v_news():
	return render_template("/radio/news.html", news = db.Newspost.select_all_desc())


@app.route('/imas-radio/no-sauce/<filename>')
def v_nosauce(filename):
	return render_template("/radio/nosauce.html", filename = filename)

# JSON ENDPOINTS
@app.route("/imas-radio/json/song_list")
def j_songlist():
	dicts = [s.__dict__ for s in db.Song.select_all()]
	return jsonify({"aaData": dicts})


@app.route("/imas-radio/json/side_image")
def j_sideimage():

	if not 'images' in session and not 'index' in session:
		bg_path = 'static/img/side_images/'

		images = preprocess_sideimages()
		random.shuffle(images)

		session['images'] = images
		session['index'] = 0
	else:

		reset = (session['index'] +1) >= len(session['images'])

		if reset:
			session['index'] = 0
		else:
			session['index'] = session['index'] +1

	return jsonify(session['images'][session['index']])


# ADMIN INTERFACE
@app.route('/admin/login', methods=['GET', 'POST'])
def a_login():
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
def a_landing():

	return render_template('radio/admin/admin.html')


@app.route('/admin/side-image-manager/')
@login_required
def a_side_image_manager():

	return render_template("radio/admin/side-image-mgr.html", 
		images = db.SideImage.select_all())


@app.route('/admin/song-data-manager/')
@login_required
def a_song_data_manager():

	return render_template("radio/admin/song-data-mgr.html",
		songs = db.Song.select_all())


@app.route('/admin/news-manager')
@login_required
def a_news_manager():

	return render_template("radio/admin/news-mgr.html",
		news = db.Newspost.select_all())


@app.route('/admin/play-file/<path:file>')
def a_play_file(file):
	folder = parser.get('music', 'music_dir')
	file = secure_filename(file)
	return send_from_directory(folder, file)


@app.route('/admin/logout')
def a_logout():
	try:
		if session['logged']:
			session.pop('logged', None)
			return redirect('/')
	except KeyError:
		return "Not logged"

#FORM ENDPOINTS
@app.route('/admin/song-data-manager/update_song', methods=['POST'])
@login_required
def f_update_song_data():
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
def f_update_image_data():
	id = request.form['image_id']
	source = request.form['image_source']

	db.SideImage.update(id, source)

	return redirect('/admin/side-image-manager')


@app.route('/admin/side-image-manager/upload_image', methods=['POST'])
@login_required
def f_upload_image():
	if "image" in request.files and request.files['image'].filename != "":

		file = request.files['image']
		filename = secure_filename(file.filename)
		folderpath = 'static/img/side_images'

		file.save(os.path.join(folderpath, filename))

		if "source" in request.form:
			db.SideImage.insert(filename, request.form["source"])
		else:
			db.SideImage.insert(filename, None)
	else:
		return "javascript:alert('malformed request')"

	return redirect("/admin/side-image-manager/")


@app.route('/admin/side-image-manager/delete_image', methods=['POST'])
@login_required
def f_delete_image():

	if "image_id" not in request.form and 'image_filename' not in request.form:
		return "javascript:alert('malformed request')"

	db.SideImage.delete_id(request.form['image_id'])
	imgpath = os.path.abspath('static/img/side_images/' + str(request.form['image_filename']))
	os.remove(imgpath)

	return redirect("/admin/side-image-manager")


@app.route("/admin/news-manager/new_newspost", methods=["POST"])
@login_required
def f_new_newspost():

	if 'newstext' not in request.form or 'author' not in request.form:
		return "javascript:alert('malformed request')"

	post = db.Newspost(request.form['author'], request.form['newstext'], datetime.datetime.now())
	db.Newspost.insert(post)

	return redirect('/admin/news-manager')


@app.route("/admin/news-manager/delete_newspost", methods=['POST'])
@login_required
def f_delete_newspost():

	if "id" not in request.form:
		return "javascript:alert('malformed request')"

	db.Newspost.delete_id(request.form['id'])

	return redirect('/admin/news-manager')


if __name__ == '__main__':
	if app.debug:
		app.jinja_env.auto_reload = True
		app.config['TEMPLATES_AUTO_RELOAD'] = True

	app.run()
