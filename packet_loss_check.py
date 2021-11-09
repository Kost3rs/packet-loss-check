import os
import sys
import time
from socket import socket, AF_INET, SOCK_DGRAM
from contextlib import contextmanager
from ping3 import verbose_ping
from datetime import datetime
from requests import get


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


stops = j = i = 0

s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

int_addr = s.getsockname()[0]
ext_addr = get("https://api.ipify.org").content.decode("utf8")
date = datetime.now().strftime("%H:%M:%S")

print(f"[{date}]  Pinging \'{ext_addr}\' from \'{int_addr}\'")
while True:
    try:
        with(suppress_stdout()):
            time.sleep(1)
            print(verbose_ping(ext_addr, src_addr=int_addr, count=1))

    except OSError:
        if not(j == i):
            stops += 1
            print(f"({stops})  LOSS")
        j = i
        j += 1

    except KeyboardInterrupt:
        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")

        print(f"Number of losses ({stops})")
        exit(-1)

    i += 1
