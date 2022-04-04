from flask import Blueprint, request, render_template
from datetime import date
from bson import json_util
import pymongo
import requests
import json
import re

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

def insertNew(hash):
    print('inserting new hash ', hash)
    today = date.today()
    print('fetching hash from Virus Total...')
    response = requests.request("GET", url+hash, headers=headers)
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
    return render_template("hashData.html", hash_JSON = newhashjson)

def updateOne(hashmd5):
    print('updating hash ', hashmd5)
    today = date.today()
    print('fetching hash from Virus Total...')
    response = requests.request("GET", url+hash, headers=headers)
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

@driver_api.route("/test")
def test():
    return "you found me!"

@driver_api.route('/hashinfo/')
def getHash():
    hash = request.args.get('hash')
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



