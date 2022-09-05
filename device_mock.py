import socket
import struct
import asyncio
from json import loads
import socketio
import sys


##############################################################################
#
# UDP MULTICAST SETTINGS
#
##############################################################################
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = False
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
        if dec and dec['mariachi_broker_ip']:
            print(f'[UDP] multicast package received!')
            try:
                ip = dec['mariachi_broker_ip']
                conn = f'http://{ip}:{port}'
                print(f'[SOCKET] Connecting to: {conn}')

                if not sioSocket.connected:
                    await sioSocket.connect(conn)
                await sioSocket.emit('msg_mariachi_ready', {'mac': sys.argv[1]})
                # await sioSocket.wait()

            except:
                print('could not conect')

##############################################################################
#
# SOCKETIO COMM SETTINGS
#
##############################################################################
port = 5000
sioUdp = socketio.AsyncClient(
    # logger=True, engineio_logger=True
)
sioSocket = socketio.AsyncClient(
    # logger=True, engineio_logger=True
)


@ sioUdp.event
async def connect():
    print('[SOCKET] connection established')
    await sioUdp.emit('message', data='detection', callback=done)
    print('[SOCKET] message sent')


async def done():
    await sioUdp.disconnect()


@ sioUdp.event
async def msg_update_sources(data):
    print('[SOCKET] message received with ', data)
    await sioUdp.emit('my response', {'response': 'my response'})


@ sioUdp.event
async def disconnect():
    print('[SOCKET] disconnected from server')


async def socketIoConnect(ip):
    conn = f'http://{ip}:{port}/'
    # print(f'Connecting to: {conn}')

    await sioUdp.connect(conn)
    await sioUdp.wait()


async def main():
    await asyncio.gather(*[
        asyncio.create_task(multicastListener()),
    ])

asyncio.run(main())
