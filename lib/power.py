import pyRAPL
from time import sleep
import threading


measure = None


def setup():
    global measure
    pyRAPL.setup() 
    measure = pyRAPL.Measurement('global')
    measure.begin()


def exit():
    global measure
    measure = None


def read_value():
    measure.end()
    joules = float(measure.result.pkg[0]) / 1e6
    measure.begin()
    return joules
