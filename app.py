#req:
#python 3
#flask
#pip freeze for venv
#render_template

from flask import Flask, request, render_template
import sqlite3
from sqlite3 import Error
import sys

app = Flask(__name__)





@app.route("/ping")
def ping():
    return "pong"


@app.route("/enterHash")
def enterHash():
    
    return render_template("enterHash.html")





@app.route("/")
@app.route("/home")
def home():

    linkA = "/selectFile"
    linkB = "/enterHash"
    linkC = "/more"
    return render_template("frontMenu.html", button_link_A = linkA, button_link_B = linkB, button_link_C = linkC,)


