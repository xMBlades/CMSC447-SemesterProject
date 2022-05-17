#req:
#python 3
#flask
#pip freeze for venv
#render_template

from flask import Flask, request, render_template, session
from driver import driver_api
from userbase import user_api
import sqlite3
from datetime import timedelta
from sqlite3 import Error
import secrets
import sys
# from flask_login import LoginManager
# login_manager = LoginManager()


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=50)
# login_manager.init_app(app)
# Session(app)

app.register_blueprint(driver_api, url_prefix='/driver')
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
app.register_blueprint(user_api, url_prefix='/users')

@app.route("/ping")
def ping():

    return "pong"

@app.route("/selectFile")
def selectFile():

    hashSearch = "/driver/fancyHash"
    returnHome = "/home"
    return render_template("selectFile.html", return_home = returnHome, hash_search = hashSearch)

@app.route("/enterHash")
def enterHash():
    
    hashSearch = "/driver/fancyHash"
    returnHome = "/home"
    return render_template("enterHash.html", return_home = returnHome, hash_search = hashSearch)

@app.route("/more")
def more():

    returnHome = "/home"
    return render_template("underConstruction.html", return_home = returnHome)

@app.route("/")
@app.route("/home")
def home():

    linkA = "/selectFile"
    linkB = "/enterHash"
    linkC = "/more"
    return render_template("frontMenu.html", button_link_A = linkA, button_link_B = linkB, button_link_C = linkC,)
@app.route("/testing")
def test():
    test = "/users/register/"
    return render_template("test", test=test)
