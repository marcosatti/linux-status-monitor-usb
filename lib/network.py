from time import sleep
import threading
import psutil


byte_counter = None


def setup():
    global byte_counter
    net_stat_start = psutil.net_io_counters(pernic=False, nowrap=True)
    byte_counter = net_stat_start.bytes_recv + net_stat_start.bytes_sent


def exit():
    global byte_counter
    byte_counter = None


def read_value():
    global byte_counter
    net_stat = psutil.net_io_counters(pernic=False, nowrap=True)
    current_byte_counter = net_stat.bytes_recv + net_stat.bytes_sent
    mebibytes = (float(current_byte_counter - byte_counter) / 1024) / 1024
    byte_counter = current_byte_counter
    return mebibytes
