from flask import Blueprint, request, render_template
from datetime import date
from bson import json_util
import pymongo
import requests
import json
import re
import math
import hashlib
# from flask_cors import CORS, cross_origin



client = pymongo.MongoClient("mongodb+srv://admin:123@cluster0.xprpc.mongodb.net/hashdb?retryWrites=true&w=majority")
db = client.Cluster0

driver_api = Blueprint('driver_api', __name__)

md5re = re.compile('^[a-fA-F0-9]{32}$')
sha1re = re.compile('^[a-fA-F0-9]{40}$')
sha256re = re.compile('^[a-fA-F0-9]{64}$')
url = "https://www.virustotal.com/api/v3/files/"
headers = {
    "Accept": "application/json",
    "x-apikey": "c6c1781bab81e19b1488b212a615a64bd9cb6318376a592d41fe79c8b703c18a",
}
headers2 = {
    "Accept": "application/json",
    "x-apikey": "382b7996b9f689b0abd1848ceefe9a31e97afdd5bd575e9766ca9d5c68322ce3"
}

headers3 = {
    "Accept": "application/json",
    "x-apikey": "40582ad863ff601e38885a20c9220954d0b41c0bb6cb99fc8e658e66893970a4"
}


def hashFile():
        f = request.files['file']
        data = f.read()
        sha256 = hashlib.sha256()
        sha256.update(data)
        f.close()
        return (sha256.hexdigest())

def insertNew(hash):
    print('inserting new hash ', hash)
    today = date.today()
    print('fetching hash from Virus Total...')
    print("GET", url+hash)
    response = requests.request("GET", url+hash, headers=headers)
    print(response.text)
    responsejson = json.loads(response.text)
    try:
        attributes = responsejson['data']['attributes']
    except KeyError:
        response = requests.request("GET", url+hash, headers=headers2)
        print(response.text)
        responsejson = json.loads(response.text)
        try:
            attributes = responsejson['data']['attributes']
        except KeyError:
            response = requests.request("GET", url+hash, headers=headers3)
            print(response.text)
            responsejson = json.loads(response.text)
            try:
                attributes = responsejson['data']['attributes']
            except KeyError:
                return 'error: 404'
    
    last_analysis_results = md5 = sha1 = sha256 = creation_date = size = type_description = signature_info = names = signers = counter_signers = hashcopyright = last_submission_date  = last_analysis_stats = ""
    if 'md5' in attributes: md5 = attributes['md5'] 
    if 'sha1' in attributes: sha1 = attributes['sha1']
    if 'sha256' in attributes: sha256 = attributes['sha256']
    if 'creation_date' in attributes: creation_date = attributes['creation_date']
    if 'size' in attributes: size = attributes['size']
    if 'type_description' in attributes: type_description = attributes['type_description']
    if 'signature_info' in attributes: signature_info = attributes['signature_info']
    if 'names' in attributes: names = attributes['names']
    if 'signature_info' in attributes and 'signers' in attributes['signature_info']: signers = attributes['signature_info']['signers']
    if 'signature_info' in attributes and 'counter_signers' in attributes['signature_info']: counter_signers = attributes['signature_info']['counter signers']
    if 'signature_info' in attributes and 'copyright' in attributes['signature_info']: hashcopyright = attributes['signature_info']['copyright']
    if 'last_submission_date' in attributes: last_submission_date = attributes['last_submission_date']
    if 'last_analysis_stats' in attributes: last_analysis_stats = attributes['last_analysis_stats']
    if 'last_analysis_results' in attributes: last_analysis_results = attributes['last_analysis_results']
    db['hashes'].insert_one({
        'md5': md5,
        'sha1': sha1,
        'sha256': sha256,
        'creation_date': creation_date,
        'size': size,
        'type_description' : type_description,
        'signature_info' : signature_info,
        'names' : names,
        'signers' : signers,
        'counter_signers': counter_signers,
        'copyright' : hashcopyright,
        'last_submission_date' : last_submission_date,
        'last_analysis_stats' : last_analysis_stats,
        'last_analysis_results' : last_analysis_results,
        'db_insertion_date' : today.strftime("%Y-%m-%d")
    })
    newhashinfo = db['hashes'].find_one({'md5' : md5})
    newhashjson = json.dumps(newhashinfo,default=json_util.default)
    return dressupJSON(newhashinfo)



def insertNewHeadless(hash):
    print('inserting new hash ', hash)
    today = date.today()
    print('fetching hash from Virus Total...')
    print("GET", url+hash)
    response = requests.request("GET", url+hash, headers=headers)
    print(response.text)
    responsejson = json.loads(response.text)
    try:
        attributes = responsejson['data']['attributes']
    except KeyError:
        response = requests.request("GET", url+hash, headers=headers2)
        print(response.text)
        responsejson = json.loads(response.text)
        try:
            attributes = responsejson['data']['attributes']
        except KeyError:
            response = requests.request("GET", url+hash, headers=headers3)
            print(response.text)
            responsejson = json.loads(response.text)
            try:
                attributes = responsejson['data']['attributes']
            except KeyError:
                return 'error: 404'
    
    last_analysis_results = md5 = sha1 = sha256 = creation_date = size = type_description = signature_info = names = signers = counter_signers = hashcopyright = last_submission_date  = last_analysis_stats = ""
    if 'md5' in attributes: md5 = attributes['md5'] 
    if 'sha1' in attributes: sha1 = attributes['sha1']
    if 'sha256' in attributes: sha256 = attributes['sha256']
    if 'creation_date' in attributes: creation_date = attributes['creation_date']
    if 'size' in attributes: size = attributes['size']
    if 'type_description' in attributes: type_description = attributes['type_description']
    if 'signature_info' in attributes: signature_info = attributes['signature_info']
    if 'names' in attributes: names = attributes['names']
    if 'signature_info' in attributes and 'signers' in attributes['signature_info']: signers = attributes['signature_info']['signers']
    if 'signature_info' in attributes and 'counter_signers' in attributes['signature_info']: counter_signers = attributes['signature_info']['counter signers']
    if 'signature_info' in attributes and 'copyright' in attributes['signature_info']: hashcopyright = attributes['signature_info']['copyright']
    if 'last_submission_date' in attributes: last_submission_date = attributes['last_submission_date']
    if 'last_analysis_stats' in attributes: last_analysis_stats = attributes['last_analysis_stats']
    if 'last_analysis_results' in attributes: last_analysis_results = attributes['last_analysis_results']
    db['hashes'].insert_one({
        'md5': md5,
        'sha1': sha1,
        'sha256': sha256,
        'creation_date': creation_date,
        'size': size,
        'type_description' : type_description,
        'signature_info' : signature_info,
        'names' : names,
        'signers' : signers,
        'counter_signers': counter_signers,
        'copyright' : hashcopyright,
        'last_submission_date' : last_submission_date,
        'last_analysis_stats' : last_analysis_stats,
        'last_analysis_results' : last_analysis_results,
        'db_insertion_date' : today.strftime("%Y-%m-%d")
    })
    newhashinfo = db['hashes'].find_one({'md5' : md5})
    newhashjson = json.dumps(newhashinfo,default=json_util.default)
    return sourcesSafe(newhashinfo)




def updateOne(hashmd5):
    print('updating hash ', hashmd5)
    today = date.today()
    print('fetching hash from Virus Total...')
    response = requests.request("GET", url+hash, headers=headers)
    print(response.text)
    responsejson = json.loads(response.text)
    try:
        attributes = responsejson['data']['attributes']
    except KeyError:
        return 'error: 404'
    last_analysis_results = md5 = sha1 = sha256 = creation_date = size = type_description = signature_info = names = signers = counter_signers = hashcopyright = last_submission_date  = last_analysis_stats = ""
    if 'md5' in attributes: md5 = attributes['md5'] 
    if 'sha1' in attributes: sha1 = attributes['sha1']
    if 'sha256' in attributes: sha256 = attributes['sha256']
    if 'creation_date' in attributes: creation_date = attributes['creation_date']
    if 'size' in attributes: size = attributes['size']
    if 'type_description' in attributes: type_description = attributes['type_description']
    if 'signature_info' in attributes: signature_info = attributes['signature_info']
    if 'names' in attributes: names = attributes['names']
    if 'signature_info' in attributes and 'signers' in attributes['signature_info']: signers = attributes['signature_info']['signers']
    if 'signature_info' in attributes and 'counter_signers' in attributes['signature_info']: counter_signers = attributes['signature_info']['counter signers']
    if 'signature_info' in attributes and 'copyright' in attributes['signature_info']: hashcopyright = attributes['signature_info']['copyright']
    if 'last_submission_date' in attributes: last_submission_date = attributes['last_submission_date']
    if 'last_analysis_stats' in attributes: last_analysis_stats = attributes['last_analysis_stats']
    if 'last_analysis_results' in attributes: last_analysis_results = attributes['last_analysis_results']
    db['hashes'].update_one({'md5':hashmd5},{
        'md5': md5,
        'sha1': sha1,
        'sha256': sha256,
        'creation_date': creation_date,
        'size': size,
        'type_description' : type_description,
        'signature_info' : signature_info,
        'names' : names,
        'signers' : signers,
        'counter_signers': counter_signers,
        'copyright' : hashcopyright,
        'last_submission_date' : last_submission_date,
        'last_analysis_stats' : last_analysis_stats,
        'last_analysis_results' : last_analysis_results,
        'db_insertion_date' : today.strftime("%Y-%m-%d")
    })
    newhashinfo = db['hashes'].find_one({'md5' : md5})
    newhashjson = json.dumps(newhashinfo,default=json_util.default)
    return render_template("hashData.html", hash_JSON = newhashjson)

def hashToJSON(hash):
    today = date.today()
    if(md5re.match(hash)):
        print('recieved md5 hash...')
        if(len(list(db['hashes'].find({'md5':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'md5':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return hashjson
            
    elif(sha1re.match(hash)):
        print('recieved sha1 hash...')
        if(len(list(db['hashes'].find({'sha1':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha1':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return hashjson
            
    elif(sha256re.match(hash)):
        print('recieved sha256 hash...')
        if(len(list(db['hashes'].find({'sha256':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha256':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return hashjson
    # return insertNew(hash)

def dressupJSON(jsn):
    dat = jsn

    neither = dat["last_analysis_stats"]["undetected"]
    malicious = dat["last_analysis_stats"]["malicious"]
    harmless = dat["last_analysis_stats"]["harmless"]
    suspicious = dat["last_analysis_stats"]["suspicious"]
    total = neither + malicious + suspicious + harmless
    threat_calc = ((malicious*1.2 - harmless*1.2) + (suspicious*0.5)) / (total)
    threat_calc *= 100
    threat_calc = min( math.floor(threat_calc), 100)

    fileStats = []
    fileStats.append(dat["names"][0])
    fileStats.append(dat["type_description"])
    fileStats.append(malicious)
    fileStats.append(suspicious)
    fileStats.append(harmless)
    fileStats.append(neither)
    fileStats.append(dat["sha256"])
    fileStats.append(dat["sha1"])
    fileStats.append(dat["md5"])
    fileStats.append(dat["type_description"])

    rslts = []
    for k in dat["last_analysis_results"].keys():
        service = dat["last_analysis_results"][k]
        tmp = []
        tmp.append(service["engine_name"])
        if service["category"] == "malicious":
            tmp.append("red")
            tmp.append(service['category'])
            tmp.append('fa-circle-xmark')
        elif service["category"] == "harmless":
            tmp.append("green")
            tmp.append(service['category'])
            tmp.append("fa-circle-check")
        else:
            tmp.append("black")
            tmp.append(service['category'])
            tmp.append("fa-circle-question")
        rslts.append(tmp)

    return render_template("hashResults.html", threat_level = threat_calc, file_info = fileStats, results = rslts)



def noHashPage():
    return "NO HASH! :("

@driver_api.route("/test")
def test():
    return "you found me!"

@driver_api.route('/hashinfo/', methods = ["GET", "POST"])
def getHash():
    if request.method == "GET":
        hash = request.args.get('hash')
    else:
        hash = hashFile()
    today = date.today()
    if(md5re.match(hash)):
        print('recieved md5 hash...')
        if(len(list(db['hashes'].find({'md5':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'md5':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return render_template("hashData.html", hash_JSON = hashjson)
            
    elif(sha1re.match(hash)):
        print('recieved sha1 hash...')
        if(len(list(db['hashes'].find({'sha1':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha1':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return render_template("hashData.html", hash_JSON = hashjson)
            
    elif(sha256re.match(hash)):
        print('recieved sha256 hash...')
        if(len(list(db['hashes'].find({'sha256':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha256':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                return updateOne(hashjson['md5'])
            return render_template("hashData.html", hash_JSON = hashjson)
            
    return insertNew(hash)



@driver_api.route('/fancyHash/', methods = ["GET", "POST"])
def rawHash():

    if request.method == "GET":
        # print('raw JSON requested')
        hash = request.args.get('hash')
    else:
        hash = hashFile()
    today = date.today()
    if(md5re.match(hash)):
        print('recieved md5 hash...')

        if(len(list(db['hashes'].find({'md5':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'md5':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return dressupJSON(hashinfo)
            
    elif(sha1re.match(hash)):
        print('recieved sha1 hash...')
        if(len(list(db['hashes'].find({'sha1':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha1':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return dressupJSON(hashinfo)
            
    elif(sha256re.match(hash)):
        print('recieved sha256 hash...')
        if(len(list(db['hashes'].find({'sha256':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha256':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return dressupJSON(hashinfo)
            
    return insertNew(hash)




def massHash(hsh):

    hash = hsh
    today = date.today()
    if(md5re.match(hash)):
        print('recieved md5 hash...')

        if(len(list(db['hashes'].find({'md5':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'md5':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return sourcesSafe(hashinfo)
            
    elif(sha1re.match(hash)):
        print('recieved sha1 hash...')
        if(len(list(db['hashes'].find({'sha1':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha1':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return sourcesSafe(hashinfo)
            
    elif(sha256re.match(hash)):
        print('recieved sha256 hash...')
        if(len(list(db['hashes'].find({'sha256':hash}))) > 0):
            print('hash exists in database!')
            hashinfo = db['hashes'].find_one({'sha256':hash})
            hashjson = json.dumps(hashinfo,default=json_util.default)
            upload_date = date.fromisoformat(hashinfo['db_insertion_date'])
            delta = today - upload_date
            print(delta, " since last update...")
            if delta.days > 30:
                updateOne(hashjson['md5'])
            return sourcesSafe(hashinfo)
            
    return insertNewHeadless(hash)





def sourcesSafe (jsn):
    dat = jsn
    neither = dat["last_analysis_stats"]["undetected"]
    malicious = dat["last_analysis_stats"]["malicious"]
    harmless = dat["last_analysis_stats"]["harmless"]
    suspicious = dat["last_analysis_stats"]["suspicious"]
    total = neither + malicious + suspicious + harmless
    threat_calc = ((malicious*1.2 - harmless*1.2) + (suspicious*0.5)) / (total)
    threat_calc *= 100
    threat_calc = min( math.floor(threat_calc), 100)
    return [neither + harmless, total]