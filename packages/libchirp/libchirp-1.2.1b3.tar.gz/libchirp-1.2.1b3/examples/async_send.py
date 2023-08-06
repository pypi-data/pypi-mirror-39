#!/usr/bin/env python3
import asyncio
from libchirp.asyncio import Chirp, Config, Loop, Message

async def send():
    for _ in range(100):
        t = []
        for i in range(100):
            t.append(chirp.send(messages[i]))
        for it in reversed(t):
            while not it.done():
                await asyncio.sleep(0.0001)
            await it

class MyChirp(Chirp):
    async def handler(self, msg):
        pass

loop = Loop(); config = Config();
config.DISABLE_ENCRYPTION = True
config.PORT = 2992
config.TIMEOUT = 1000
messages = []
for _ in range(100):
    message = Message()
    message.data = b'hello'
    message.address = "127.0.0.1"
    message.port = 2998
    messages.append(message)
aio_loop = asyncio.get_event_loop()
try:
    try:
        chirp = MyChirp(loop, config, aio_loop)
        fut = asyncio.ensure_future(send())
        aio_loop.run_until_complete(fut)
    finally:
        chirp.stop()
finally:
    loop.stop()
