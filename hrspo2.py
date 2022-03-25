import random
import time

#Use this as a library to return an array of data from the HRSPO2 sensor.

hr = []
spo2 = []

#def get_hrspo2():
#    for i in range(998):
#        _hr = random.randint(60,100)
#        _spo2 = random.randint(90,100)
#        hr.append(_hr)
#        spo2.append(_spo2)
#        time.sleep(0.01)
#    
#    return hr

#import time
import max30100
#These spaces represent other code for sensors being used


sensor = max30100.MAX30100() #Create max30100 sensor object instance | Put these back in
sensor.enable_spo2() #enable SPO2 measurements | Put these back in


def get_hrspo2():
    global hr, spo2
    for i in range(199):
        sensor.read_sensor()
        sensor.ir, sensor.red #Sensor returns two values, each of which will be used for unique measurements
        _hr = int(sensor.ir / 100) - 130 #Subtractions here are a result of manual calibration
        _spo2 = int(sensor.red / 100) - 68
        
        hr.append(_hr)
        spo2.append(_spo2)
        time.sleep(0.5)
        
    returning_hr = hr
    returning_spo2 = spo2
    
    hr = []
    spo2 = []
    
    return returning_hr,returning_spo2