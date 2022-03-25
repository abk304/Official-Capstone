import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import busio
import digitalio
import board
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#Importing gspread and initializing google sheet
import gspread
sa = gspread.service_account()
sh = sa.open("Capstone_datatransmission_101")
wks = sh.worksheet("SheetBeta")

plt.ion() #allows for plot to refresh or close
en = [19, 24]
GPIO.setmode(GPIO.BCM)
GPIO.setup(en, GPIO.OUT)
GPIO.output(en[0], 0)
GPIO.output(en[1], 0)

inS = [12, 16, 20, 21]
GPIO.setup(inS, GPIO.OUT)

outS = [26, 17, 27, 22]
GPIO.setup(outS, GPIO.OUT)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

channel = AnalogIn(mcp, MCP.P1)

uniform_data = np.arange(256).reshape(16, 16)
#uniform_data[1,1] = 2

def matrixsensor():
    count = 0
    while count < 30:
        count = count + 1
        for x in range (0, 15):
            #print(format(x,"04b")[0], end = '')
        
            GPIO.output(inS[3], int(format(x,"04b")[0]))
            GPIO.output(inS[2], int(format(x,"04b")[1]))
            GPIO.output(inS[1], int(format(x,"04b")[2]))
            GPIO.output(inS[0], int(format(x,"04b")[3]))
        
            for y in range (0,15):
                GPIO.output(outS[3], int(format(y,"04b")[0]))
                GPIO.output(outS[2], int(format(y,"04b")[1]))
                GPIO.output(outS[1], int(format(y,"04b")[2]))
                GPIO.output(outS[0], int(format(y,"04b")[3]))
                uniform_data[y,x] = channel.value
            
        result = uniform_data.ravel()
        #print("New resulting array: ", result)

        newarr = np.array_split(result, 16)
        newarr0 = newarr[0].tolist()
        newarr1 = newarr[1].tolist()
        newarr2 = newarr[2].tolist()
        newarr3 = newarr[3].tolist()
        newarr4 = newarr[4].tolist()
        newarr5 = newarr[5].tolist()
        newarr6 = newarr[6].tolist()
        newarr7 = newarr[7].tolist()
        newarr8 = newarr[8].tolist()
        newarr9 = newarr[9].tolist()
        newarr10 = newarr[10].tolist()
        newarr11 = newarr[11].tolist()
        newarr12 = newarr[12].tolist()
        newarr13 = newarr[13].tolist()
        newarr14 = newarr[14].tolist()
        newarr15 = newarr[15].tolist()
    
        arr = newarr0+newarr1+newarr2+newarr3+newarr4+newarr5+newarr6+newarr7+newarr8+newarr9+newarr10+newarr11+newarr12+newarr13+newarr14+newarr15
        
        
        ax = sns.heatmap(uniform_data, linewidth=0.5,cmap="YlGnBu")
        
        plt.clf()
        plt.show(block=False)
        time.sleep(1)
        #plt.pause(1)
        #plt.clf()
        #plt.close()
        
        data = wks.range('A2:P17')
            
        for i, val in enumerate(arr):
            data[i].value = val
                
        wks.update_cells(data)
    plt.close()
    