from bottle import get, route, template, run, request
from plugin import websocket
from server import GeventWebSocketServer
from pymongo import MongoClient

users=[]

@route('/')
def logreg():
    return template('signlog')

@route('/signup')
def sign():
    return template('signlog')

@route('/login')
def log():
    return template('signlog')

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
dict2={}
@route('/websocket',apply=[websocket])
def chat(ws):
    print (ws)
    client=MongoClient()
    db=client.dtbs
    strin=db.usrinf1.find()
    for bla in strin:
        strin1=bla['Usr']
        break
    print(strin1)
    db.usrinf1.drop()
    users.append(ws)
    print(users)
    sender=strin1
    str=sender+" is active"
    str1=sender+" is not active"
    usr.append(sender)
    for u1 in usr:
        print (u1)
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
    user_on_off=ws.receive()
    datetime1=ws.receive()
    c1=0
    c4=0
    if((sender in dict)==False):
        dict[sender]=[]
    if((sender in dict1)==False):
        dict1[sender]=[]
    if(user_on_off=='Online'):
        for d in dict[sender]:
            c4=0
            ws.send(d)
            ws.send("(Send by "+dict1[sender][c1]+" at "+datetime1+" )")
            for us in users:
                if(usr[c4]==dict1[sender][c1]):
                    us.send("(Received by "+sender+" at "+datetime1+" )")
                    break
                c4=c4+1
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
        if(msg==None):
            break
        receiver=ws.receive()
        print(msg)
        print(receiver)
        if((receiver in dict)==False):
            dict[receiver]=[]
        if((receiver in dict1)==False):
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
        c2=0
        db.Log.insert({
        "message_status":str2
        })
        if msg is not None:
            ws.send(msg)
            ws.send("(Send to "+receiver+" at "+datetime+" )")
            db.Log.insert({
            "message_status":"Message by "+sender+" was sent to "+receiver
            })
            for u in users:
                if(c>len(usr)-1):
                    break
                if(usr[c]==receiver):
                    c2=1
                    print("usr "+usr[c])
                    print("rec "+receiver)
                    print(u)
                    u.send(msg)
                    datetime1=datetime
                    u.send("(Send by "+sender+" at "+datetime1+" )")
                    ws.send("(Received by "+receiver+" at "+datetime+" )")
                    db.Main_coll.update({'info_for':sender,'sender':sender,'receiver':receiver,'datetime':datetime},{'$set':{'status':'Received'}})
                    db.Main_coll.update({'info_for':receiver,'sender':sender,'receiver':receiver,'datetime':datetime},{'$set':{'datetime':datetime1}})
                    db.Log.insert({
                    "message_status":str3+" at "+datetime1
                    })
                    break
                c=c+1
            if(c2==0):
                dict[receiver].append(msg)
                dict1[receiver].append(sender)
            for s in dict[receiver]:
                print(s)
            for s1 in dict1[receiver]:
                print(s1)
        else:
            break
    users.remove(ws)
    usr.remove(sender)
    db.Log.insert({
    "user_status":str1
    })

@get('/ws_signlog', apply=[websocket])
def ws_signlog(ws):
    client = MongoClient()
    db = client.dtbs
    while(True):
        usrnm=ws.receive()
        if(usrnm is None):
            break
        usrid=ws.receive()
        pwd=ws.receive()
        stat=ws.receive()
        if(stat=='Signup'):
            if(db.usrinf.find_one({'$and':[
            {"UserID":usrid}
            ]}) is None):
                db.usrinf.insert({
                "Username":usrnm,
                "UserID":usrid,
                "Password":pwd,
                "Status":stat
                })
                db.usrinf1.insert({"Usr":usrid})
                str5=usrnm+" signed up with User ID: "+usrid
                db.Log.insert({"sign_up":str5})
                ws.send("Signup successfull, redirecting...")
            else:
                ws.send("Account already exists, please try again with different credentials")
        if(stat=='Login'):
            if(db.usrinf.find_one({'$and':[
            {"UserID":usrid},{"Password":pwd},{"Username":usrnm}
            ]}) is not None):
                db.usrinf1.insert({"Usr":usrid})
                str6=usrnm+" logged in with User ID: "+usrid
                db.Log.insert({"login":str6})
                ws.send("Login successfull, redirecting...")
            else:
                ws.send("Wrong credentials, please try again!")



run(host='localhost', port=8080, server=GeventWebSocketServer)