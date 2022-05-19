#req:
#python 3
#flask
#pip freeze for venv
#render_template

from flask import Flask, request, render_template, session
from driver import driver_api, massHash
from userbase import user_api, SESSION
import sqlite3
from datetime import timedelta
from sqlite3 import Error
import secrets
import sys
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
# from flask_login import LoginManager
# login_manager = LoginManager()
# g.user = {}
QUEUE = []
RESULTS = {}
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

@app.route("/selectFolder")
def selectFolder():

    hashSearch = "/driver/fancyHash"
    returnHome = "/home"
    uid = -1
    try:
        uid = SESSION[request.cookies.get('userID')][0]
    except:
        return render_template("loginPlease.html", return_home = returnHome)
    return render_template("selectFolder.html", return_home = returnHome, hash_search = hashSearch, userID = uid)

@app.route("/enterHash")
def enterHash():
    
    hashSearch = "/driver/fancyHash"
    returnHome = "/home"   
    return render_template("enterHash.html", return_home = returnHome, hash_search = hashSearch)

@app.route("/enterLink")
def enterLink():
    
    hashSearch = "/driver/scanLink"
    returnHome = "/home"   
    return render_template("enterLink.html", return_home = returnHome, hash_search = hashSearch)

@app.route("/more")
def more():

    returnHome = "/home"
    return render_template("underConstruction.html", return_home = returnHome)

@app.route("/")
@app.route("/home")
def home():

    linkA = "/selectFile"
    linkB = "/enterHash"
    linkC = "/enterLink"
    linkD = "/selectFolder"
    linkE = "/scanResults"
    linkF = "/users/register"
    fname = ""
    lname = ""
    user_page = ""
    img_src = ""
    logged_in = False

    try:
        tmp = SESSION[request.cookies.get('userID')][:]
        # print("here!")
        fname = tmp[2]
        lname =  tmp[3]
        user_page = ""
        img_src =  tmp[4]
        logged_in = True
    except:
        logged_in = False


    return render_template("frontMenu.html", button_link_A = linkA, button_link_B = linkB, button_link_C = linkC,  button_link_D = linkD, button_link_E = linkE, button_link_F = linkF, logged_in = logged_in, fname = fname, lname = lname, user_page = user_page, img_src = img_src)

@app.route("/scanResults", methods = ["GET"])
def scanResults():
    results = -1
    remainingFilesInQueue = 0
    errorMsgFlag = -1
    userNum = ""
    try:
        tmp = request.cookies.get('userID')
        # print(tmp)
        tmp = SESSION[request.cookies.get('userID')]
        # print(tmp)
        tmp = str(SESSION[request.cookies.get('userID')][0])
        print(tmp)
        print(RESULTS)
        errorMsgFlag = 0
        userNum = tmp[:]
        results = RESULTS[str(SESSION[request.cookies.get('userID')][0])]
        # print(results)
    except:
        return render_template("massResults.html", results = "", remaining_files = errorMsgFlag)
    counter = 0
    resultList = ""
    for q in QUEUE:
        if str(q["user"]) == userNum:
            remainingFilesInQueue += 1
    pass

    for r in results:

        rslt_id = r[1]
        rslt_name = r[0]
        hosts_cleared = r[2]
        hostsTotal = r[3]
        file_type = "KNOWN"
        color = "green"
        try:
            if (int(r[3]) == 0):
                hosts_cleared = "0"
                hostsTotal = "0"
                file_type = "UNIQUE"
            elif (int(r[2])/int(r[3]) <= 0.8):
                color = "red"
        except ValueError:
            hosts_cleared = "0"
            hostsTotal = "0"
            file_type = "UNIQUE"

        counter += 1
        resultList = resultList + render_template("resultBox.html.j2", result_name =  rslt_name, result_id = rslt_id, hosts_cleared = hosts_cleared, hostsTotal = hostsTotal, file_type = file_type, color = "green")
    return render_template("massResults.html", results = resultList, remaining_files = remainingFilesInQueue)


@app.route("/scanResultsR", methods = ["GET"])
def scanResultsRefreshable():
    results = -1
    remainingFilesInQueue = 0
    errorMsgFlag = -1
    userNum = ""
    try:
        tmp = request.cookies.get('userID')
        # print(tmp)
        tmp = SESSION[request.cookies.get('userID')]
        # print(tmp)
        tmp = str(SESSION[request.cookies.get('userID')][0])
        print(tmp)
        print(RESULTS)
        errorMsgFlag = 0
        userNum = tmp[:]
        results = RESULTS[str(SESSION[request.cookies.get('userID')][0])]
        # print(results)
    except:
        return render_template("massResultsRefresh.html", results = "", remaining_files = errorMsgFlag)
    counter = 0
    resultList = ""
    for q in QUEUE:
        if str(q["user"]) == userNum:
            remainingFilesInQueue += 1
    pass

    for r in results:

        rslt_id = r[1]
        rslt_name = r[0]
        hosts_cleared = r[2]
        hostsTotal = r[3]
        file_type = "KNOWN"
        color = "green"
        try:
            if (int(r[3]) == 0):
                hosts_cleared = "0"
                hostsTotal = "0"
                file_type = "UNIQUE"
            elif (int(r[2])/int(r[3]) <= 0.8):
                color = "red"
        except ValueError:
            hosts_cleared = "0"
            hostsTotal = "0"
            file_type = "UNIQUE"

        counter += 1
        resultList = resultList + render_template("resultBox.html.j2", result_name =  rslt_name, result_id = rslt_id, hosts_cleared = hosts_cleared, hostsTotal = hostsTotal, file_type = file_type, color = "green")
    return render_template("massResultsRefresh.html", results = resultList, remaining_files = remainingFilesInQueue)




@app.route("/enqueue", methods = ["POST"])
def enqueue():
    tmp = {"name": request.form.get('name'), "hash": request.form.get('hash'), "user": request.form.get('user')}
    QUEUE.append(tmp)
    print("ADDED  {name:", request.form.get('name'), ", hash:", request.form.get('hash'), ", user:", request.form.get('user'), "}")
    return "Okay!"

def dequeue():
    tmp = None
    try:
        tmp = QUEUE.pop(0)
    except:
        # print("empty queue")
        return "Empty"

    scanRslt = massHash(tmp["hash"])
    try:
        RESULTS[tmp["user"]].append([tmp['name'], tmp['hash'], scanRslt[0], scanRslt[1]])

    except KeyError:
        try:
            RESULTS[tmp["user"]].append([tmp['name'], tmp['hash'], 0, 0])
        except :
            RESULTS.update({tmp["user"] : [[tmp['name'], tmp['hash'], 0, 0]]})
    pass
    # print("REMOVED  ", tmp["name"], " from queue for user", tmp["user"])
    # QUEUE.append(tmp)
    return "Okay!"


scheduler = BackgroundScheduler()
scheduler.add_job(func=dequeue, trigger="interval", seconds=10)
scheduler.start()