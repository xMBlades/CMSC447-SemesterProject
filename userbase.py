from flask import Flask, Blueprint, request, render_template, url_for, send_from_directory
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
# from flask_login import LoginManager
# login_manager.login_view = 'login'
# login_manager = LoginManager()

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

	
	mycursor = mydb.cursor()

	

except:
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="8281E76A144CF7EC18D8030B6142134F", #MD5 hash of UserDatabaseUsername
	  password="69BBCAB266F45C077F1362B104BDBF1E", #MD5 hash of UserDatabasePassword
	  port = '3360',
	  database= USER_DB_NAME
	)

	mycursor = mydb.cursor()

	# mycursor.execute("CREATE DATABASE " +  USER_DB_NAME)
# mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), password VARCHAR(255),  imgURL VARCHAR(255), salt VARCHAR(255))")	






user_api = Blueprint('user_api', __name__)



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

		emptyField = str(pickle.dumps([]))

		sql = "INSERT INTO users (username, fname, lname, email, password,  imgURL, salt, requests) VALUES (%s, %s, %s, %s, %s,  %s, %s)"
		val = (username, fname, lname, email, storablePW, usrImgUrl, salt, emptyField)
		mycursor.execute(sql, val)

		mydb.commit()


		return  "record #" + str(mycursor.rowcount) + " inserted."
        
	else:
		return render_template("registrationPage.html")


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@user_api.route('/login', methods=['GET', 'POST'])
def login():
	if  request.method == "POST":
		username = request.form.get('usrname')
		password = request.form.get('pass')
	    # info = json.loads(request.data)
	    # username = info.get('username', 'guest')
	    # password = info.get('password', '') 
	    # user = User.objects(name=username,
	    #                     password=password).first()
	    # if user:
	    #     login_user(user)
	    #     return jsonify(user.to_json())
	    # else:
	    #     return jsonify({"status": 401,
	    #                     "reason": "Username or Password Error"})
		return "POST REQUEST"
	else:
		return render_template("loginPage.html", register_url = "/register/")
