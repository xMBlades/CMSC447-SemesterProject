from flask import Blueprint, request, render_template, url_for, send_from_directory
from datetime import date
from bson import json_util
import requests
import json
import re
import math
import hashlib
import os
import mysql.connector
from werkzeug.utils import secure_filename
USER_DB_NAME = "userDB"

# mycursor = None
# try:
# 	mydb = mysql.connector.connect(
# 		host="localhost",
# 		user="8281E76A144CF7EC18D8030B6142134F", #MD5 hash of UserDatabaseUsername
# 		password="69BBCAB266F45C077F1362B104BDBF1E", #MD5 hash of UserDatabasePassword
# 		database= USER_DB_NAME
# 	)


# 	mycursor = mydb.cursor()

# 	mycursor.execute("CREATE TABLE users (name VARCHAR(255), address VARCHAR(255))")

# except:
# 	mydb = mysql.connector.connect(
# 	  host="localhost",
# 	  user="8281E76A144CF7EC18D8030B6142134F", #MD5 hash of UserDatabaseUsername
# 	  password="69BBCAB266F45C077F1362B104BDBF1E" #MD5 hash of UserDatabasePassword
# 	)

# 	mycursor = mydb.cursor()

# 	mycursor.execute("CREATE DATABASE " +  USER_DB_NAME)






user_api = Blueprint('user_api', __name__)

UPLOAD_FOLDER = "static/images/userImgs"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


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





# usrname: 123456
# email: 123456
# pass: 123456
# cpass: 123456
# fileToUpload: (binary)
# fname: 123
# lname: 123
# submit: Submit

@user_api.route('/register/', methods = ["GET", "POST"])
def registerUsr():
	if  request.method == "POST":
		username = request.args.get('usrname')
		email = request.args.get('email')
		password = request.args.get('pass')
		fileToUpload = request.args.get('pass')
		usrImgUrl = storeUserImg(request.files['fileToUpload'])
		fname = request.args.get('fname')
		lname = request.args.get('lname')
		return usrImgUrl
        
	else:
		return render_template("registrationPage.html", form_action = "#")


