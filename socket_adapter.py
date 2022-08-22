from aiohttp import web
import asyncio
from contextvars import ContextVar
from socket import gethostbyname, gethostname
import click

app = web.Application()

runner = web.AppRunner(app)
VAR = ContextVar('VAR', default='default')
my_ip = gethostbyname(gethostname())
my_port = 5000


async def handler(request):
    click.echo(f"In handler!")
    return web.Response(text='TEST')


class WebServer():

    def __init__(self):
        super()

    @staticmethod
    async def run():

        await runner.setup()
        click.echo(f"Opening TCPSite on {my_ip}:{my_port}")
        site = web.TCPSite(runner, my_ip, my_port)
        await site.start()

        while True:
            await asyncio.sleep(3600)  # sleep forever


app.router.add_get('/', handler)
app.router.add_get('', handler)
