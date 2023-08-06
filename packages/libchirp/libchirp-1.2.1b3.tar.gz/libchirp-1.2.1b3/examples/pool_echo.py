#!/usr/bin/env python3
from concurrent.futures import Future
from libchirp.pool import Chirp, Config, Loop
import sys

class MyChirp(Chirp):
    pass

loop = Loop(); config = Config()
config.DISABLE_ENCRYPTION = True
# Workers are usually asynchronous
config.SYNCHRONOUS = False
try:
    chirp = MyChirp(loop, config)
    try:
        sys.stdin.read()
    finally:
        chirp.stop()
finally:
    loop.stop()
