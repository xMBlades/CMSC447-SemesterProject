#req:
#python 3
#flask
#pip freeze for venv
#render_template

from flask import Flask, request, render_template
from driver import driver_api
import sqlite3
from sqlite3 import Error
import sys

app = Flask(__name__)

app.register_blueprint(driver_api, url_prefix='/driver')

@app.route("/ping")
def ping():

    return "pong"

@app.route("/selectFile")
def selectFile():

    hashSearch = "/driver/hashinfo"
    returnHome = "/home"
    return render_template("selectFile.html", return_home = returnHome, hash_search = hashSearch)

@app.route("/enterHash")
def enterHash():
    
    hashSearch = "/driver/hashinfo"
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


