from bottle import get, route, template, run, request#Importing bottle framework
from plugin import websocket#Importing websocket functionality
from server import GeventWebSocketServer#Importing server
from pymongo import MongoClient#Importing pymongo
from random import randint
import signal
import sys

users=[]#Making an empty list

@route('/')#Defining a default route
def logreg():
    return template('signlog')#returning a template when the route is entered

@route('/signup')#Defining a named route
def sign():
    return template('signlog')

@route('/login')
def log():
    return template('signlog')

@route('/admin')
def adm():
    return template('admin')

@route('/adm')
def adm1():
    return template('adm')

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
dict={}#Definign an empty dictionary
dict1={}
dict2={}


def signal_handler(signal, frame):#Defining a signal handler for handing Ctrl+C
    print('You pressed Ctrl+C!')
    client=MongoClient()
    db=client.dtbs
    db.usrinf3.delete_many({})#Removing all documents from the collection
    sys.exit(0)#Exiting system
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')#Printing on console

@route('/websocket',apply=[websocket])
def chat(ws):
    print (ws)
    client=MongoClient()
    db=client.dtbs
    strin=db.usrinf1.find()#findind all documents
    strin1="0123456789xabcdefgx9876543210"
    for val in strin:
        strin1=val['Usr']
        break
    if(strin1=="0123456789xabcdefgx9876543210"):#checking if the user directly accesses chat page without login
        return
    print(strin1)
    db.usrinf1.drop()
    users.append(ws)
    db.usrinf3.insert({"Usr":strin1})#Number of online users
    print(users)
    sender=strin1
    str=sender+" is active"
    str1=sender+" is not active"
    usr.append(sender)
    for u1 in usr:
        print (u1)
    collection=db.Log
    collection=db.Main_coll#creating collection
    db.Log.insert({
    "new_usr":"New User Enters"
    })
    db.Log.insert({
    "user_status":str
    })
    db.Main_coll.insert({#Insering in main collection
    "new_usr":"New User Enters"
    })
    user_on_off=ws.receive()
    datetime1=ws.receive()
    c1=0
    c4=0
    if((sender in dict)==False):#Checking if sender already in dictionary, it is used for multiple closing and opening from same account
        dict[sender]=[]
    if((sender in dict1)==False):
        dict1[sender]=[]
    if(user_on_off=='Online'):#Checking if sender online
        print(dict[sender])
        print(dict1[sender])
        for d in dict[sender]:
            c4=0
            ws.send(d)#Sending pending messages
            ws.send("(Send by "+dict1[sender][c1]+" at "+datetime1+" )")#sending Sent report
            for us in users:
                if(usr[c4]==dict1[sender][c1]):
                    us.send("(Received by "+sender+" at "+datetime1+" )")#Sending delivered report to sender
                    break
                c4=c4+1
            db.Main_coll.update({'info_for':dict1[sender][c1],'sender':dict1[sender][c1],'receiver':sender},{'$set':{'status':'Received'}})
            db.Main_coll.update({'info_for':sender,'sender':dict1[sender][c1],'receiver':sender},{'$set':{'datetime':datetime1}})
            db.Log.insert({
            "message_status":"Message by "+dict1[sender][c1]+" was delivered to "+sender
            })
            c1=c1+1
        dict[sender].clear()#clearing dictionary
        dict1[sender].clear()
        print(dict[sender])
        print(dict1[sender])
    print("abc")
    while(True):
        msg=ws.receive()#receiving message from user
        if(msg==None or msg=="Offline1234abc5678def90ghij"):#Checking if user has refreshed or closed tab
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
            ws.send(msg)#Sending message to sender
            ws.send("(Send to "+receiver+" at "+datetime+" )")
            db.Log.insert({
            "message_status":"Message by "+sender+" was sent to "+receiver
            })
            for u in users:
                if(c>len(usr)-1):
                    break
                if(usr[c]==receiver):#checking for receiver in list
                    c2=1
                    print("usr "+usr[c])
                    print("rec "+receiver)
                    print(u)
                    u.send(msg)#if receiver found, message is send
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
            if(c2==0):#if receiver isnt found, that is, is inactive or doesn't have an account
                dict[receiver].append(msg)#message is stored in a dictionary
                dict1[receiver].append(sender)
            for s in dict[receiver]:
                print(s)
            for s1 in dict1[receiver]:
                print(s1)
        else:
            break
    users.remove(ws)#removing user, now offline
    usr.remove(sender)
    db.usrinf3.delete_one( { "Usr": strin1 } )#user now not in online users list
    db.Log.insert({#inserting logged out status
    "user_status":str1
    })

@get('/ws_signlog', apply=[websocket])
def ws_signlog(ws):
    client = MongoClient()
    db = client.dtbs
    while(True):
        usrnm=ws.receive()#receiving username
        if(usrnm is None):#checking if connection is closed
            break
        usrid=ws.receive()#receiving usrid and other values
        pwd=ws.receive()
        stat=ws.receive()
        if(stat=='Signup'):#Checking the value of stat, here signup
            if(db.usrinf.find_one({'$and':[#Finding the document in 'usrinf' colection with user id equal to the one entered
            {"UserID":usrid}
            ]}) is None):#if no user id found, i.e, no duplicate, then data inserted in database
                db.usrinf.insert({
                "Username":usrnm,
                "UserID":usrid,
                "Password":pwd,
                "Status":stat,
                "Type":"User"
                })
                db.usrinf2.insert({"Usr":usrid})#Used to later find out number of total users
                db.usrinf1.insert({"Usr":usrid})
                str5=usrnm+" signed up with User ID: "+usrid
                db.Log.insert({"sign_up":str5})#Storing in log
                ws.send("Signup successfull, redirecting...")
            else:
                ws.send("Account already exists, please try again with different credentials")#If account already exists, then declined
        if(stat=='Login'):#Used for finding if Login entered
            if(db.usrinf.find_one({'$and':[#Finding a document to see if it matches the given credentials
            {"UserID":usrid},{"Password":pwd},{"Username":usrnm}
            ]}) is not None):#If it matches, info is stored and user logged in
                db.usrinf1.insert({"Usr":usrid})
                str6=usrnm+" logged in with User ID: "+usrid
                db.Log.insert({"login":str6})
                ws.send("Login successfull, redirecting...")
            else:
                ws.send("Wrong credentials, please try again!")#Otherwise error message displayed


@get('/ws_adm', apply=[websocket])#Defining functionality for a given route
def adm(ws):#Function to handle functionality
    client = MongoClient()
    db = client.dtbs
    while(True):
        str1=ws.receive()#Receiving from adm.tpl a "Send" message which indicates to send current database values of total and online users
        if(str1 is None):
            break
        if(str1=="Send"):
            n=db.usrinf2.count()#Counting documents in the 'usrinf2' collection
            n1=db.usrinf3.count()
            ws.send("abc"+str(n)+":"+str(n1))#Sending the data in the form of a unique string, so that data can be extracted in adm.tpl

@get('/refresh')
def refresh():
    client = MongoClient()#Creating an instance of MongoDB
    db = client.dtbs#Defining a database
    db.Log.drop()#Clearing an entire collection
    db.Main_coll.drop()
    db.usrinf.drop()
    db.usrinf1.drop()
    db.usrinf2.drop()
    db.usrinf3.drop()

run(host='192.168.43.29', port=8080, server=GeventWebSocketServer)#Running the server and listening on the given port of the mentioned url