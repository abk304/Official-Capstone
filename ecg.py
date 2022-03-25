import random
import time

#Use this as a library to return an array of data from the ECG sensor.

ecg = []

#def get_ecg():
#    for i in range(998):
#        number = random.randint(0,30)
#        numbers.append(number)
#        time.sleep(0.01)
#    
#    return numbers

# Real ECG stuff
import busio
import digitalio
import board
import time

import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)

#Define a channel
channel = AnalogIn(mcp,MCP.P0)
def get_ecg():
    global ecg
    for i in range(998):
        _ecg = channel.voltage
        ecg.append(_ecg)
        time.sleep(0.02)
    
    returning_ecg = ecg
    ecg = []
    return returning_ecg