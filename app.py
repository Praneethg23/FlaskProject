from flask import Flask, request,make_response,jsonify
import json
import secrets
import datetime
import copy
import threading

posts = []
users = []
app = Flask(__name__)
threadLock=threading.Lock()
@app.post("/user")
def postUsers():
    try:
        request.get_json()
    except:
        response = make_response('bad request', 400)
        return response
    if('username' not in request.get_json() or 'name' not in request.get_json()):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    username = request.get_json().get('username')
    name = request.get_json().get('name')
    if(not type(username) is str or not type(name) is str):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    usernames=[]
    with threadLock:
        usernames = [d['username'] for d in users]
    if(username in usernames):
        response = make_response(jsonify({"err":"forbidden"}), 403)
        return response
    user_id = 0
    if(len(users)>0):
        user_id=users[len(users)-1]['user_id']+1
    user_key = secrets.token_urlsafe(16)
    with threadLock:
        keys = [d['user_key'] for d in users]
    while(user_key in keys):
        user_key = secrets.token_urlsafe(16)
    user={}
    user['user_id'] = user_id
    user['username'] = username
    user['name'] = name
    user['user_key'] = user_key
    with threadLock:
        users.append(user)
    return user
@app.get('/user/<username>')
def getUser(username):
    flag = False
    u = {}
    with threadLock:
        for user in users:
            if(user['username'] == username):
                u = copy.deepcopy(user)
                flag = True
                break
    if(flag):
        del u['user_key']
        return u
    else:
        response = make_response(jsonify({"err":"not found"}), 404)
        return response
@app.put('/user/<userkey>')
def putUser(userkey):
    try:
        request.get_json()
    except:
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    if('username' not in request.get_json() and 'name' not in request.get_json()):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    flag = False
    ind = 0
    with threadLock:
        for i in range(0,len(users)):
            if(users[i]['user_key']==userkey):
                ind =i
                flag = True
                break
        if(flag):
            username = users[ind]['username']
            name = users[ind]['name']
            if('name' in request.get_json()):
                name = request.get_json().get('name')
            if('username' in request.get_json()):
                username = request.get_json().get('username')
                usernames = [d['username'] for d in users]
                if(username in usernames):
                    response = make_response(jsonify({"err":"forbidden"}), 403)
                    return response
            users[ind]['username'] = username
            users[ind]['name'] = name
            u = copy.deepcopy(users[ind])
            del u['user_key']
            return u
        else:
            response = make_response(jsonify({"err":"forbidden"}), 403)
            return response

@app.post("/post")
def postPosts():
    try:
        request.get_json()
    except:
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    if('msg' not in request.get_json()):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    msg = request.get_json().get('msg')
    if(not type(msg) is str):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    id = 0
    with threadLock:
        if(len(posts)>0):
            id=posts[len(posts)-1]['id']+1
        key = secrets.token_urlsafe(16)
        keys = [d['key'] for d in posts]
        while(key in keys):
            key = secrets.token_urlsafe(16)
        timestamp = datetime.datetime.now().isoformat()
        post={}
        post['id'] = id
        post['key'] = key
        post['timestamp'] = timestamp
        post['msg'] = msg
        if('user_key' in request.get_json() and 'user_id' in request.get_json()):
            flag = False
            ind = 0
            for i in range(0,len(users)):
                if(users[i]['user_key']==request.get_json().get('user_key') and users[i]['user_id']==request.get_json().get('user_id')):
                    ind =i
                    flag = True
                    break
            if(flag):
                post['username']=users[ind]['username']
                post['user_key'] = users[ind]['user_key']
                post['user_id'] = users[ind]['user_id']
                print(post)
            else:
                response = make_response(jsonify({"err":"not found"}), 404)
                return response
        posts.append(post)
        print(post)
        return post
@app.get("/post/<id>")
def getPost(id):
    try:
        flag = False
        p = {}
        with threadLock:
            for post in posts:
                if(post['id']==int(id)):
                    p = copy.deepcopy(post)
                    flag = True
                    break
            if(flag):
                del p['key']
                if('user_key' in p.keys()):
                    del p['user_key']
                return p
            else:
                response = make_response(jsonify({"err":"not found"}), 404)
                return response
    except:
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
@app.delete("/post/<id>/delete/<key>")
def delPost(id,key):
    flag = False
    idflag = False
    p = {}
    with threadLock:
        for i in range(0,len(posts)):
            if(posts[i]['id']==int(id) and key == posts[i]['key']):
                p = copy.deepcopy(posts[i])
                del posts[i]
                flag = True
                break
            elif(posts[i]['id']==int(id)):
                idflag = True
        if(flag):
            del p['msg']
            if('user_key' in p.keys()):
                del p['user_key']
            return p
        elif(idflag):
            response = make_response(jsonify({"err":"forbidden"}), 403)
            return response
        else:
            response = make_response(jsonify({"err":"not found"}), 404)
            return response
@app.delete("/post/<id>/delete/user/<userkey>")
def delPostUser(id,userkey):
    flag = False
    idflag = False
    p = {}
    with threadLock:
        for i in range(0,len(posts)):
            if('user_key' not in posts[i].keys()):
                continue
            if(posts[i]['id']==int(id) and userkey == posts[i]['user_key']):
                p = copy.deepcopy(posts[i])
                del posts[i]
                flag = True
                break
            elif(posts[i]['id']==int(id)):
                idflag = True
        if(flag):
            del p['msg']
            if('user_key' in p.keys()):
                del p['user_key']
            return p
        elif(idflag):
            response = make_response(jsonify({"err":"forbidden"}), 403)
            return response
        else:
            response = make_response(jsonify({"err":"not found"}), 404)
            return response
@app.get("/post/search/time")
def getPostsTime():
    try:
        request.get_json()
    except:
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    if('endTime' not in request.get_json() and 'startTime' not in request.get_json()):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    flag = 0
    try:
        if('endTime' in request.get_json()):

            datetime.datetime.strptime(request.get_json().get('endTime'),'%m/%d/%Y %H:%M:%S')
            flag+=1
        if('startTime' in request.get_json()):
            datetime.datetime.strptime(request.get_json().get('startTime'),'%m/%d/%Y %H:%M:%S')
            flag+=2
    except :
        response = make_response(jsonify({"err" : "bad request"}), 400)
        return response
    res = []
    with threadLock:
        if(flag==1):
            endTime = datetime.datetime.strptime(request.get_json().get('endTime'),'%m/%d/%Y %H:%M:%S')
            for post in posts:
                timestamp = datetime.datetime.fromisoformat(post['timestamp'])
                if( timestamp <= endTime):
                    p = copy.deepcopy(post)
                    del p['key']
                    if('user_key' in p.keys()):
                        del p['user_key']
                    res.append(p)
        elif(flag==2):
            startTime= datetime.datetime.strptime(request.get_json().get('startTime'),'%m/%d/%Y %H:%M:%S')
            for post in posts:
                timestamp = datetime.datetime.fromisoformat(post['timestamp'])
                if( timestamp>= startTime):
                    p = copy.deepcopy(post)
                    del p['key']
                    if('user_key' in p.keys()):
                        del p['user_key']
                    res.append(p)
        elif(flag==3):
            endTime = datetime.datetime.strptime(request.get_json().get('endTime'),'%m/%d/%Y %H:%M:%S')
            startTime= datetime.datetime.strptime(request.get_json().get('startTime'),'%m/%d/%Y %H:%M:%S')
            for post in posts:
                timestamp = datetime.datetime.fromisoformat(post['timestamp'])
                if( timestamp <= endTime and timestamp>=startTime):
                    p = copy.deepcopy(post)
                    del p['key']
                    if('user_key' in p.keys()):
                        del p['user_key']
                    res.append(p)
        else:
            response = make_response(jsonify({"err":"bad request"}), 400)
            return response
        if(len(res)>0):
            return res
        else:
            response = make_response(jsonify({"err":"not found"}), 404)
            return response
@app.get("/post/search/user/<id>")
def getPostsUser(id):
    try:
        int(id)
    except:
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    res = []
    with threadLock:
        for post in posts:
            if('user_id' not in post.keys()):
                continue
            if(post['user_id']==int(id)):
                p = copy.deepcopy(post)
                del p['key']
                if('user_key' in p.keys()):
                    del p['user_key']
                res.append(p)
        if(len(res)>0):
            return res
        else:
            response = make_response(jsonify({"err":"not found"}), 404)
            return response
@app.get("/post/search/msg/<text>")
def getPostsText(text):
    if(text.strip()==''):
        response = make_response(jsonify({"err":"bad request"}), 400)
        return response
    res = []
    with threadLock:
        for post in posts:
            if(text in post['msg']):
                p = copy.deepcopy(post)
                del p['key']
                if('user_key' in p.keys()):
                    del p['user_key']
                res.append(p)
    if(len(res)>0):
        return res
    else:
        response = make_response(jsonify({"err":"not found"}), 404)
        return response
    