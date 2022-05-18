from flask import Flask, Blueprint, request, render_template, url_for, send_from_directory, make_response, redirect, g
from datetime import date
from bson import json_util
import requests
import json
import re
import math
import secrets
import hashlib
import os
import random
import pickle
import mysql.connector
from werkzeug.utils import secure_filename
#test
from driver import driver_api

# from flask_login import LoginManager
# login_manager.login_view = 'login'
# login_manager = LoginManager()
SESSION = {}
USER_DB_NAME = "userDB"
UPLOAD_FOLDER = "static/images/userImgs"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
SALT_LENGTH = 32

mycursor = None
try:
	mydb = mysql.connector.connect(
		host="localhost",
		user="8281E76A144CF7EC18D8030B6142134F", #MD5 hash of UserDatabaseUsername
		password="69BBCAB266F45C077F1362B104BDBF1E", #MD5 hash of UserDatabasePassword
		port = '3360',
		database= USER_DB_NAME
	)

	
	mycursor = mydb.cursor(buffered=True)

	

except:
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="8281E76A144CF7EC18D8030B6142134F", #MD5 hash of UserDatabaseUsername
	  password="69BBCAB266F45C077F1362B104BDBF1E", #MD5 hash of UserDatabasePassword
	  port = '3360',
	  database= USER_DB_NAME
	)

	mycursor = mydb.cursor(buffered=True)

	# mycursor.execute("CREATE DATABASE " +  USER_DB_NAME)
# mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), password VARCHAR(255),  imgURL VARCHAR(255), salt VARCHAR(255))")	






user_api = Blueprint('user_api', __name__)
user_api.register_blueprint(driver_api, url_prefix='/driver')


@user_api.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def storeUserImg(file):
	if file.filename == '':
		return ''
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		return UPLOAD_FOLDER + "/" + filename



def getUser(cookie):
	try:
		return SESSION[cookie]
	except:
		return None


@user_api.route('/register/', methods = ["GET", "POST"])
def registerUsr():
	if  request.method == "POST":
		username = request.form.get('usrname')
		email = request.form.get('email')
		password = request.form.get('pass')
		usrImgUrl = storeUserImg(request.files['fileToUpload'])

		fname = request.form.get('fname')
		lname = request.form.get('lname')
		salt = secrets.token_urlsafe(SALT_LENGTH//2) #Generate a BASE64 salt to add to the end of the user's password, hash password with that token to store.

		sha256 = hashlib.sha256()
		sha256.update((password + salt).encode('UTF-8'))

		storablePW = sha256.hexdigest()

		emptyField = ''

		sql = "INSERT INTO users (username, fname, lname, email, password,  imgURL, salt, requests) VALUES (%s, %s, %s, %s, %s,  %s, %s, %s)"
		val = (username, fname, lname, email, storablePW, usrImgUrl, salt, emptyField)
		mycursor.execute(sql, val)

		mydb.commit()


		return  "record #" + str(mycursor.rowcount) + " inserted."
        
	else:
		return render_template("registrationPage.html")


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@user_api.route('/logout', methods=['GET'])
def logout():
	userID = request.cookies.get('userID')
	SESSION.pop(userID)
	return redirect("../")

@user_api.route('/login', methods=['GET', 'POST'])
def login():
	if  request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')
		print("Login Attempted for", username)

		sql = "SELECT * FROM users WHERE username LIKE '" + username + "'"
		# val = (username, fname, lname, email, storablePW, usrImgUrl, salt, emptyField)
		mycursor.execute(sql)

		mydb.commit()

		# print(sql)
		myresult = mycursor.fetchall()
		# counter = 0
		# print(myresult[0][5], myresult[0][7])

		sha256 = hashlib.sha256()
		sha256.update((password +  myresult[0][7]).encode('UTF-8'))

		storablePW = sha256.hexdigest()

		if (storablePW == myresult[0][5]):
			print("Login Succeed")
			resp = make_response(redirect("../"))
			token = secrets.token_urlsafe(32)
			resp.set_cookie('userID', token)
			SESSION.update({token: [myresult[0][0], username, myresult[0][2], myresult[0][3], myresult[0][6]]})
			return resp
		else:
			resp = make_response(render_template("loginPage.html", register_url = "/register/", alert = True))
			return resp
	else:
		return render_template("loginPage.html", register_url = "/register/", alert = False)
