from serial import Serial
from sliplib import encode
from struct import pack
import time
import asyncio


port = None


def setup(this_port):
    global port
    port = Serial(port=this_port)
    

def write_status(status):
    data = status.SerializeToString()
    length = 2 + len(data) 
    encoded = encode(pack('<H', length) + data)
    port.write(encoded)
    port.flush()


async def read_main(period, stop_cb):
    time_instant = time.time()

    while not stop_cb():
        # Poll for bytes in the buffer, then try to read them.
        if port.in_waiting > 0:
            message = port.read_until()
            message = message.decode('utf-8')
            duration = time.time() - time_instant
            print(f'[{duration:.3f}] ' + message, end='')
        await asyncio.sleep(period)


def exit():
    global port
    port.close()
    port = None
