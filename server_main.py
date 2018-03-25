from bottle import get, route, template, run, request
from plugin import websocket
from server import GeventWebSocketServer

users=set()

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

@route('/websocket',apply=[websocket])
def chat(ws):
    print (ws)
    users.add(ws)
    print(users)
    while(True):
        msg=ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else:
            break
    users.remove(ws)

run(host='localhost', port=8080, server=GeventWebSocketServer)