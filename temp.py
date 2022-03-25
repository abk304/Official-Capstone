import random
import time

from w1thermsensor import W1ThermSensor
from kivy.clock import Clock

#Use this as a library to return an array of data from the HRSPO2 sensor.
global _temp
temp = []
temperature_sensor = W1ThermSensor()

#def get_temp():
#    for i in range(998):
#        _temp = random.randint(60,100)
#        temp.append(_temp)
#        time.sleep(0.01)
#    
#    return temp

#def local_temp(dt):
#    global _temp
#    __temp = temperature_sensor.get_temperature()
#    _temp.append(__temp)

def get_temp():
    global temp
    for i in range(40):
        #Clock.schedule_once(local_temp,1.5)
        _temp = temperature_sensor.get_temperature()
        temp.append(_temp)
        time.sleep(1.5)
        
    returning_temp = temp
    temp = []
    return returning_temp