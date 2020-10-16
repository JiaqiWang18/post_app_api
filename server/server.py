from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "postapp-48b9d",
  "private_key_id": "e8f563a73c9a7e6d540f7c60dfff98e046090f0f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCeie7Xm183wd8N\nYITDYTNN22m7TaZY8h8/JKqZ/TT5yJnZ985nCQkjMFXSVwbUVz3vvlplBouyLjH4\nooGVVIjEkZyJWsq4AKvWf/j0Ie5280tiwvyCVSt0qJIicFMKuCug3DUKwSO2mWDR\nb7KVxfrJChV6Ppc8+tF4i6nTLWv12T2F7QJNEC/WgCWQmWCyDH94hsr5GbwzU/px\nZRfvSOqcSyUuxwGDRCsKLHICqxUIoPaoyFs9Efq9fpYSldxzpL19BcictXAzS8Bt\ns5sQ4TthEPy/XVksl4urAINpMA7Mbp/hJh4Nr1MsnZsyqRkVn18VtnJAA1XEZGTO\n+BdLxFY9AgMBAAECggEAGqCZliphH3UHMNC7c7JNYt/9felAjXNbFqiio7rwrRxJ\nZN/XUZxlpbyeSXX27m6ZtzzOI2YqS9qw52zp3Uolr3gyZapzXly0f9IeHujdC6r4\nyCVuMji6U/1lD/Y0KFp+72VU3lHKnQZdScfcI4YtRRtVuKKvFZ2d1YSFmTOpjJC0\nZs0qPxf0YVxzqshHjdDFdkBd+LlWtLd9FtLuLJdLh4rF4RbEnv61rH3toVT+0hFA\nFhV2IKx4ghOJRHJTfOVJqDC4tP5CMRLv+XPXAH+TwpTMJWvTWGOiKJaQjlyTgJbc\nYhx3gZmkhOIM+n07OP7sHwFT9PDvEvxNSv1TUII2+QKBgQDdmiImk1f6t2xd8gqt\nc0BJlBStjjbeX6IgsYrjTqKsgDp5+N+n69WCb5Yqavglw4eDqY+55Zn8W8dhM3cf\neeImVVshkRzpF++Aqx3zeuIXPK+bDfcSCLOSHrwaRE+E699c772Sw9fFuhSwSZP7\nQRD3ZnVW+k4s3G9UVLDfnPm/WQKBgQC3JdXkkCXpy4LzEIaWT5Z5QcOk9CZj4xkl\nowk28mxROCipHuAeKyfTA80WtI17GoNycVCpbp6Cb6VTQfwvXifo+xXC07t6tXGE\nTtqx/dbOjRtsg6Kr0QTjgx8zixQjZregFuuUUQrieFSCoo+pIA1eyNU0aEPPBiAA\nr1ZSakq1hQKBgQCtRdPmLdfhJoMJgjRvI2rlHXB9tHGat1RiE/Dxg48XKryOmtbm\nyjSMZQwZ5sJZZOYVQQQs6ybYeDsR+dfvOLJoHt2/BWSBrkGLbkFhHHikisMUjnre\nEwe1/Wo/b6Jt4LEqThsBIzkYVkPPA/k9wMava+HcPKPb2BEE86PJdUijIQKBgGa2\n5n2YRlsXkupk40ZbfmWk92eEsh8lF05fYGSbkxn95/fpZAIna99Ra20Hd62J0hyV\n5ooPiwBWQx8ti5S5NqLYZnzsqGGKbw6n9skKNrWCt9WlAc9gm2BJgm8y2el8yxES\nqa51wSgAGk1lhDJy0mzNL52DuDvcEIixzTTNffbNAoGBAIDyk6T4lpB/ZRjGsLK0\nKJ4s5n0skshJzKcez62ySy7DbtAXtbUBjqngwGb5hevQiT8yUUMhXbj2jbrcnBG/\nrLaBLPKXsXkXKKsCm33Fvx3TtNkGsqO+CDxLucqzzSdkbkfJ3OvBCdugo+09pJfw\nxFWzysoq8K3Nb9wFlDo1BkAC\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-yefvh@postapp-48b9d.iam.gserviceaccount.com",
  "client_id": "104453231818358255262",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yefvh%40postapp-48b9d.iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://postapp-48b9d.firebaseio.com/'
})
root = db.reference()

def getObject(post_type=None):
    if(post_type is None or post_type == "all"):
        return root.get()["post_app"]["post_app"]["post"]
    output = list()
    pk_list = json.loads(root.child("post_app").child("post_app").child("category").child(post_type).get())
    for key in pk_list:
        output.append(getPostObjWithPk(key))
    return output

def getPostObjWithPk(pk):
    return root.child("post_app").child("post_app").child("post").child(str(pk)).get()

def getAuthorObjWithUsername(username):
    return root.child("post_app").child("post_app").child("users").child(str(username)).get()

def upVotePostWithPk(pk):
    currentVal =  int(root.child("post_app").child("post_app").child("post").child(str(pk)).child("votes").get())
    newObj = getPostObjWithPk(pk)

    if not currentVal:
        newObj["votes"]="1"
    else:
        newObj["votes"] = str(currentVal+1)
    root.child("post_app").child("post_app").child("post").child(str(pk)).set(newObj)

def downVotePostWithPk(pk):
    currentVal =  int(root.child("post_app").child("post_app").child("post").child(str(pk)).child("votes").get())
    newObj = getPostObjWithPk(pk)

    if not currentVal:
        newObj["votes"]="-1"
    else:
        newObj["votes"] = str(currentVal-1)
    root.child("post_app").child("post_app").child("post").child(str(pk)).set(newObj)

def sortPostsByVote(descend,post_type):
    if descend ==0: #latest first
        return list(reversed(getObject(post_type)))
    elif descend == 1: #popular first
        descend = True
    elif descend == 2:#latest last
        return getObject(post_type)
    else: #popular last
        descend = False
    return sorted([x for x in getObject(post_type) if x is not None], key=lambda k: int(k['votes']),reverse=descend)

def getCategoryNames():
    return list(root.child("post_app").child("post_app").child("category").get().keys())

@app.route('/')
def home_page():
    data  = getObject()
    return render_template('home.html',post_obj=data ,categories=getCategoryNames())

@app.route('/all/<order>')
def allPosts(order=0):
    post_type = request.args.get('type')
    return jsonify(sortPostsByVote(int(order),post_type))

@app.route('/posts/<pk>')
def post_detail(pk=None):
    data = getPostObjWithPk(pk)
    return render_template('post_detail.html', post_obj=data)

@app.route('/posts/<pk>/upvote')
def upvote_post(pk=None):
    upVotePostWithPk(pk)
    return "done"

@app.route('/posts/<pk>/downvote')
def downvote(pk=None):
    downVotePostWithPk(pk)
    return "done"

@app.route('/author/<author>')
def user_posts(author=None):
    author=author.replace('"','')
    post_obj=[]
    for post_dict in getObject():
        if post_dict is not None and post_dict["author"].replace('"',"") == author:
            post_obj.append(post_dict)
    return render_template('user_posts.html',post_obj=post_obj,author=getAuthorObjWithUsername(author))

@app.route('/posts/<pk>/votes')
def getVoteWithPk(pk=None):
    return getPostObjWithPk(pk)["votes"]


if __name__ == '__main__':
    #testing func, to run server, go to upper directory and run wsgi.py
    print(getObject("health"))