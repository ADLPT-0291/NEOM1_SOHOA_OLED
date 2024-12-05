from pyA20.gpio import gpio
from pyA20.gpio import port
import os
import time
from time import sleep

gpio.init()

kich_modul4g = 9 # chan 37
gpio.setcfg(kich_modul4g, gpio.OUTPUT)
gpio.output(kich_modul4g, 1)
print('on nguon!')