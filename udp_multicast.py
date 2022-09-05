from socket import AF_INET, SOCK_DGRAM, IPPROTO_UDP, IPPROTO_IP, IP_MULTICAST_TTL, gethostbyname, gethostname
import socket
from json import dumps
import asyncio
from tabnanny import verbose
import click

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2
sock = socket.socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, MULTICAST_TTL)
# get our IP. Be careful if you have multiple network interfaces or IPs
my_ip = gethostbyname(gethostname())
RETRY_LIMIT = 10


class Multicast:

    def __init__(self):
        pass

    def send(self):
        message = {'my_ip': my_ip}
        data = dumps(message)
        sock.sendto(data.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
        if self.verbose:
            print(
                f"[UDP] Multicasting local IP {my_ip}:5000 for devices to connect via socket.io")

    @classmethod
    async def cast(cls, scan, verbose):
        retries = 0
        self = cls()
        self.verbose = verbose
        while retries < RETRY_LIMIT:
            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(None, self.send)
            await asyncio.sleep(1)
            retries += 1
            print(
                f"[UDP] multicast #{retries}")

        click.echo('[UDP] END              ')
