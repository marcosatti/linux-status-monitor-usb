import argparse
import sys
import traceback 
import signal
import asyncio
import psutil
import cputemp.cputemp as cputemp
import lib.driver as driver
import lib.power as power
import lib.network as network
import lib.samba as samba
from lib_protobuf.status_pb2 import Status


parser = argparse.ArgumentParser(description='Status reporter driver')
parser.add_argument('port', help='serial port that the reporter display device is connected to')
parser.add_argument('--period', type=float, default=1.0, help='the reporting period (default every second)')
args = parser.parse_args()

print('Start status monitor')


# Signal handler.
stop = False

def sigint_handler(_code, _frame):
    global stop
    stop = True

signal.signal(signal.SIGINT, sigint_handler)


# Setup libraries.
driver.setup(args.port)
power.setup()
network.setup()


async def status_main():
    while not stop:
        status = Status()
        status.cpu = int(psutil.cpu_percent())
        status.cpu_power = int(power.read_value() / args.period)
        status.temperature = int(cputemp.readTemp() / 1000)
        status.network = int(network.read_value() / args.period)
        status.samba_users_connected = samba.get_current_users_count()
        status.samba_files_opened = samba.get_open_files_count()

        driver.write_status(status)
        await asyncio.sleep(args.period)


async def main():
    status_main_task = status_main()
    read_main_task = driver.read_main(lambda: stop)
    await asyncio.gather(read_main_task, status_main_task)


asyncio.run(main())


# Teardown libraries.
network.exit()
power.exit()
driver.exit()


print('Exit status monitor')
