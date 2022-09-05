from aiohttp import web
import socketio
import eventlet
import asyncio
from threading import Thread
from socket import gethostbyname, gethostname

my_ip = gethostbyname(gethostname())
my_port = 5000
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('[SOCKET] connect ', sid)


@sio.event
def my_message(sid, data):
    print('[SOCKET] message ', data)


@sio.event
def disconnect(sid):
    print('[SOCKET] disconnect ', sid)


class WebServer():

    def __init__(self):
        super()

    @staticmethod
    def listen():
        eventlet.wsgi.server(eventlet.listen((my_ip, my_port)), app)

    @staticmethod
    async def run():
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, WebServer.listen)
