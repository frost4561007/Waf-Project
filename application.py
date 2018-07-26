from flask import Flask, render_template, request, redirect, json, url_for, request, abort
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
import os
import sqlite3
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
application = app= Flask(__name__)
app.secret_key = "mysecretkey"
google_blueprint = make_google_blueprint(client_id='58639801113-hpseuv9faul6e21npea4qh55eqar7jrj.apps.googleusercontent.com', client_secret='g5rknjPxezf4sR-MC5G1qo4i', scope=['profile', 'email'], redirect_url='/google')
app.register_blueprint(google_blueprint, url_prefix='/google_login')
github_blueprint = make_github_blueprint(client_id='2ff15c228d87b9cdc1e9', client_secret='383b00b2fafca9bb1bb87fea5bd247b77b7e37e2', redirect_url='/github')
app.register_blueprint(github_blueprint, url_prefix='/github_login')

@application.route('/')
def home():
	return render_template('homepage.html')

@application.route('/google')
def google_login():
	if not google.authorized:
		return redirect(url_for('google.login'))
	resp = google.get("/oauth2/v2/userinfo")
	assert resp.ok, resp.text
	email=resp.json()["email"]
	name=resp.json()["name"]
	picture=resp.json()["picture"]
	return render_template('welcome.html',email=email,name=name,picture=picture)

@application.route('/github')
def github_login():
	if not github.authorized:
		return redirect(url_for('github.login'))
	resp = github.get("/user")
	assert resp.ok, resp.text
	email=resp.json()["email"]
	name=resp.json()["login"]
	picture=resp.json()["avatar_url"]
	return render_template('welcome.html',email=email,name=name,picture=picture)

@application.route('/login_action', methods=["POST","GET"])
def login_action():
	user_name=request.form['username']
        pass_word=request.form['password']
	database='users.db'
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("Select * from user where username='%s' and password='%s'" %(user_name, pass_word))
	data=c.fetchall()
	conn.close()
	return "<h1>Wecome {}</h1>".format(data)

@application.route('/comment', methods=["POST","GET"])
def comment():
	comm=request.form['comment']
	return comm

@application.route('/Welcome')
def welcome():
	return render_template('welcome.html')

if __name__ == "__main__":
	application.debug=True
	application.run(host='0.0.0.0', port='5000')
