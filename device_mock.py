import socket
import struct
import asyncio
from json import loads
import socketio
from enum import Enum


##############################################################################
#
# UDP MULTICAST SETTINGS
#
##############################################################################
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = True
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


async def multicastListener():
    while True:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, sock.recv, 1000)
        dec = loads(res.decode('utf-8'))
        if dec and dec['my_ip']:
            print(f'[UDP] multicast package received!')
            try:
                ip = dec['my_ip']
                conn = f'http://{ip}:{port}'
                print(f'[SOCKET] Connecting to: {conn}')

                await sio.connect(conn)
                await sio.emit('sub.symbol', {'symbol': 'VDS_USDT'})
                await sio.wait()
            except:
                print('could not conect')

##############################################################################
#
# SOCKETIO COMM SETTINGS
#
##############################################################################
port = 5000
sio = socketio.AsyncClient(
    # logger=True, engineio_logger=True
)


@ sio.event
async def connect():
    print('[SOCKET] connection established')
    await sio.emit('message', data='detection', callback=done)
    print('[SOCKET] message sent')


async def done():
    await sio.disconnect()


@ sio.event
async def my_message(data):
    print('[SOCKET] message received with ', data)
    await sio.emit('my response', {'response': 'my response'})


@ sio.event
async def disconnect():
    print('[SOCKET] disconnected from server')


async def socketIoConnect(ip):
    conn = f'http://{ip}:{port}/'
    # print(f'Connecting to: {conn}')

    await sio.connect(conn)
    await sio.wait()


async def main():
    await asyncio.gather(*[
        asyncio.create_task(multicastListener()),
    ])

asyncio.run(main())
