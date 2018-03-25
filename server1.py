from bottle import get, route, template, run, request
from plugin import websocket
from server import GeventWebSocketServer
from pymongo import MongoClient

users=[]

@route('/')
def logreg():
    return template('login')

@route('/admin')
def adm():
    return template('admin')

@route('/superuser')
def supusr():
    return template('superuser')

@route('/supervisor')
def supvor():
    return template('supervisor')

@route('/user')
def usr():
    return template('user')

usr=[]
dict={}
dict1={}
@route('/websocket',apply=[websocket])
def chat(ws):
    print (ws)
    users.append(ws)
    print(users)
    sender=ws.receive()
    str=sender+" is active"
    str1=sender+" is not active"
    usr.append(sender)
    for u1 in usr:
        print (u1)
    client=MongoClient()
    db=client.dtbs
    collection=db.Log
    collection=db.Main_coll

    db.Log.insert({
    "new_usr":"New User Enters"
    })
    db.Log.insert({
    "user_status":str
    })
    db.Main_coll.insert({
    "new_usr":"New User Enters"
    })
    dict[sender]=[]
    dict1[sender]=[]
    user_on_off=ws.receive()
    datetime1=ws.receive()
    c1=0
    if(user_on_off=='Online'):
        for d in dict[sender]:
            ws.send(d)
            ws.send("(Send by "+sender+" at "+datetime1+" )")
            db.Main_coll.update({'info_for':dict1[sender][c1],'sender':dict1[sender][c1],'receiver':sender},{'$set':{'status':'Received'}})
            db.Main_coll.update({'info_for':sender,'sender':dict1[sender][c1],'receiver':sender},{'$set':{'datetime':datetime1}})
            db.Log.insert({
            "message_status":"Message by "+dict1[sender][c1]+" was delivered to "+sender
            })
            c1=c1+1
        for d in dict[sender]:
            dict[sender].remove(d)
        for d1 in dict1[sender]:
            dict1[sender].remove(d1)
    print("abc")
    while(True):
        msg=ws.receive()
        receiver=ws.receive()
        print(msg)
        print(receiver)
        dict[receiver]=[]
        dict1[receiver]=[]
        str2=sender+" sent a message to "+receiver
        str3="Message by "+sender+" was delivered to "+receiver
        datetime=ws.receive()
        db.Main_coll.insert({
        "info_for":sender,
        "msg":msg,
        "sender":sender,
        "receiver":receiver,
        "datetime":datetime,
        "status":"Sent"
         })
        db.Main_coll.insert({
        "info_for":receiver,
        "msg":msg,
        "sender":sender,
        "datetime":datetime,
        "receiver":receiver
        })
        c=0
        db.Log.insert({
        "message_status":str2
        })
        if msg is not None:
            for u in users:
                if(usr[c]==receiver):
                    print("usr "+usr[c])
                    print("rec "+receiver)
                    print(u)
                    u.send(msg)
                    datetime1=datetime
                    u.send("(Send by "+sender+" at "+datetime1+" )")
                    db.Main_coll.update({'info_for':sender,'sender':sender,'receiver':receiver},{'$set':{'status':'Received'}})
                    db.Main_coll.update({'info_for':receiver,'sender':sender,'receiver':receiver},{'$set':{'datetime':datetime1}})
                    db.Log.insert({
                    "message_status":str3+" at "+datetime1
                    })
                else:
                    dict[receiver].append(msg)
                    dict1[receiver].append(sender)
                c=c+1
        else:
            break
    users.remove(ws)
    usr.remove(sender)
    db.Log.insert({
    "user_status":str1
    })

run(host='localhost', port=8080, server=GeventWebSocketServer)