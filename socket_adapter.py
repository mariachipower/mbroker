from aiohttp import web
import socketio
import eventlet
import asyncio
from threading import Thread
from socket import gethostbyname, gethostname

host_ip = gethostbyname(gethostname())
host_port = 5000
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('[SOCKET] Connect ', sid)


@sio.event
def msg_mariachi_ready(sid, data):
    print('[SOCKET] Message ', data)


@sio.event
def disconnect(sid):
    print('[SOCKET] Disconnect ', sid)


class WebServer():

    def __init__(self):
        super()

    @staticmethod
    def listen():
        eventlet.wsgi.server(eventlet.listen((host_ip, host_port)), app)

    @staticmethod
    async def run():
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, WebServer.listen)
