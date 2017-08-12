from flask import Flask, redirect, render_template, request, make_response,\
	session, abort

import random
import sys
import os
import configparser
import base64

import util

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read('config.ini')

app.config['music_path'] = parser.get('music', 'music_dir')

app.secret_key = parser.get('app', 'secret_key')
app.debug = parser.getboolean('app','debug')

ws_url = parser.get("app","ws_url")
side_image_list = None
song_list = None


# MAIN PAGES
@app.route('/')
def root():
	return render_template('index.html')


@app.route('/imas-radio/')
def radio():
	return render_template('/radio/imas-radio.html',
		mobile = util.is_mobile(request.headers.get('User-Agent')),
		ws_url = ws_url)


@app.route('/imas-radio/song-list/')
def song_list_page():
	return render_template('radio/song-list.html',
		song_list = song_list,
		show_filenames = 'show_filenames' in request.args)

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
def admin_page():
	try:
		logged = session['logged']
		
	except KeyError:
		abort(403)

	return render_template('radio/admin/admin.html')


@app.route('/admin/logout')
def admin_logout():
	try:
		if session['logged']:
			session.pop('logged', None)
			return redirect('/')
	except KeyError:
		return "Not logged"
		

# UTILITIES
@app.route('/imas-radio/util/side-image/')
def random_idol():
	bg_path = 'static/img/side_images/'

	global side_image_list

	if not 'side_images' in session.keys() and not \
		'side_images_index' in session.keys():
		
		session['side_images'] = []
		session['side_images_index'] = 0

		session['side_images'] = random.sample(side_image_list,\
			len(side_image_list))
	else:
		if session['side_images_index'] != len(session['side_images']) - 1:
			session['side_images_index'] = session['side_images_index'] + 1
		else:
			session['side_images_index'] = 0

	image_to_serve = bg_path +\
		session['side_images'][session['side_images_index']]

	if 'base64' in request.args:

		with open(image_to_serve , "rb") as image:
			b64 = base64.b64encode(image.read()).decode("utf-8")
			return str("data:image/png;base64," + b64)

	else:
		response = make_response(redirect(image_to_serve))
		response.headers['Cache-Control'] = 'max-age=0'

		return response


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error/404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('error/500.html',
		admin_email = parser.get("contact", "admin_email")),500


@app.before_first_request
def appsetup():
	global side_image_list
	global song_list

	side_image_list = os.listdir('static/img/side_images')
	song_list = util.listsongs()
	
if __name__ == '__main__':
	app.run(host='0.0.0.0')
