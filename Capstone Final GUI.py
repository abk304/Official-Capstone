# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 17:34:40 2022

@author: AbhayKaushik
"""

#CAPSTONE GUI PART THREE BITCHESSS
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import StringProperty
#Look for screen transitions!!!
from kivy.config import Config
Config.set('graphics', 'width','800')
Config.set('graphics', 'height','400')
Config.set('graphics', 'resizable', False)

import time
import random

#Set window to fixed size
from kivy.core.window import Window
Window.clearcolor=(52/255,170/255,235/255,1)

#Importing thread
import threading

#Testing data display
#import randomg
#import time

#Getting pyplot and other things to graph ECG on GUI
from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg

#Getting font
from kivy.core.text import LabelBase
LabelBase.register(name='CL1960',fn_regular='data/Chalet London Nineteen Sixty Font.ttf')
LabelBase.register(name='CNY1960',fn_regular='data/Chalet New York Nineteen Sixty Font.ttf')
#font_name = "CL1960"
#font_name = "CNY1960"
#Importing self-written library that will return sensor data
import ecg
import hrspo2
import temp
import matrixsensor

#Importing gspread and initializing google sheet
import gspread
sa = gspread.service_account()
sh = sa.open("Capstone_datatransmission_101")
wks = sh.worksheet("SheetAlpha")

#File that stores patient's results
#file = open('displayvalues')

#Here are coded the welcome screen, the home screen where the user
#can select anything they want and the main test screens where the 
#users can commence the tests. 
Builder.load_string("""

                    
<WelcomeScreen>:
    
    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"                  Welcome to the Dr.Assist Kit! \\n To start, please select the home button below."
            font_name:"CNY1960"
            font_size:30
            bold: True
            pos: (0,0)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
        
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.13,0.26)
            pos:(340,40)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
        
        Label:
            text:"Home"
            font_name:"CNY1960"
            bold:True
            font_size:32
            pos:(-10,-180)
        
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
<HomeScreen>:

    FloatLayout:
        size: root.width, root.height

        Label:
            text:"Home Screen"
            font_name:"CNY1960"
            bold:True
            font_size:32
            pos:(0,150)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/ecg-button-b.png"
            background_down:"data/ecg-button-down-b.png"
            size_hint:(0.12,0.2)
            pos:(210,220)
            border:(0,0,0,0)
            on_release:
                root.manager.current = 'ecgscreen'
                root.manager.transition.direction = 'up'
                
        Label:
            text:"ECG Test"
            font_name:"CL1960"
            bold:False
            font_size:28
            pos:(-140,0)
            
        Button:
            background_normal:"data/heartrate-spo2-button-b.png"
            background_down:"data/heartrate-spo2-button-down-b.png"
            size_hint:(0.12,0.2)
            pos:(500,220)
            border:(0,0,0,0)
            on_release:
                root.manager.current = 'hrspo2screen'
                root.manager.transition.direction = 'up'
            
        Label:
            text:"Heartrate-SPO2 Test"
            font_name:"CL1960"
            bold:False
            font_size:28
            pos:(155,0)
        
        Button:
            background_normal:"data/stemp-button-b.png"
            background_down:"data/stemp-button-down-b.png"
            size_hint:(0.12,0.2)
            pos:(210,80)
            border:(0,0,0,0)
            on_release:
                root.manager.current = 'tempscreen'
                root.manager.transition.direction = 'up'
                
        Label:
            text:"Temperature Test"
            font_name:"CL1960"
            bold:False
            font_size:28
            pos:(-140,-140)
        
        Button:
            background_normal:"data/matrixsensor-button-b.png"
            background_down:"data/matrixsensor-button-down-b.png"
            size_hint:(0.12,0.2)
            pos:(500,80)
            border:(0,0,0,0)
            on_release:
                root.manager.current = 'matrixscreen'
                root.manager.transition.direction = 'up'
                
        Label:
            text:"Matrix Pressure Test"
            font_name:"CL1960"
            bold:False
            font_size:28
            pos:(160,-140)
        
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
<ECGScreen>:
    
    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
        
        Label:
            text:"The ECG test will tell your doctor \\n how fast your heart is beating and \\n give them information about the \\n rythm and regularity of your heart \\n beats. Please remain seated while \\n the test is in progress."
            font_name:"CL1960"
            font_size:18
            bold: False
            pos: (150,50)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/disp-desc-border.png"
            size_hint:(0.8,1.8)
            pos:(80,-120)
            
        Image:
            source:"data/ecg-disp-pic.png"
            size_hint:(0.45,0.45)
            pos:(70,130)
        
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='down'
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
        Button:
            background_normal:"data/sbegin-test-image.png"
            background_down:"data/sbegin-test-image-down.png"
            size_hint:(0.25,0.25)
            pos:(465,100)
            on_release:
                root.manager.current = 'ecgscreentests1'
                root.manager.transition.direction='up'
            
<HRSPO2Screen>:
    
    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Heartrate & SPO2 Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
        
        Label:
            text:"The heartrate and SPO2 test will \\n tell your doctor how fast your \\n heart is beating and the percentage \\n of oxygen-carrying hemoglobin in \\n your blood. Please remain seated \\n while the test is in progress."
            font_name:"CL1960"
            font_size:18
            bold: False
            pos: (150,50)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/disp-desc-border.png"
            size_hint:(0.8,1.8)
            pos:(80,-120)
            
        Image:
            source:"data/heartrate-spo2-disp-pic.png"
            size_hint:(0.45,0.45)
            pos:(70,130)
        
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='down'
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
        Button:
            background_normal:"data/sbegin-test-image.png"
            background_down:"data/sbegin-test-image-down.png"
            size_hint:(0.25,0.25)
            pos:(465,100)
            on_release:
                root.manager.current = 'hrspo2screentests1'
                root.manager.transition.direction= 'up'
            
<TempScreen>:
    
    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Temperature Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
        
        Label:
            text:"The temperature test will tell \\n your doctor your body temperature. \\n Please remain seated while the test \\n is in progress and do not remove \\n the temperature probe until you are \\n prompted to do so."
            font_name:"CL1960"
            font_size:18
            bold: False
            pos: (150,50)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/disp-desc-border.png"
            size_hint:(0.8,1.8)
            pos:(80,-120)
            
        Image:
            source:"data/sthermometer-disp-pic.png"
            size_hint:(0.45,0.45)
            pos:(70,130)
        
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='down'
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
        Button:
            background_normal:"data/sbegin-test-image.png"
            background_down:"data/sbegin-test-image-down.png"
            size_hint:(0.25,0.25)
            pos:(465,100)
            on_release:
                root.manager.current = 'tempscreentests1'
                root.manager.transition.direction = 'up'
            
<MatrixScreen>:
    
    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Matrix Pressure Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
        
        Label:
            text:"The matrix pressure sensor test \\n will allow your doctor to \\"feel\\" \\n any areas on your skin that may \\n have bumps or lumps. Please \\n remain seated while the test is \\n in progress."
            font_name:"CL1960"
            font_size:18
            bold: False
            pos: (150,50)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/disp-desc-border.png"
            size_hint:(0.8,1.8)
            pos:(80,-120)
            
        Image:
            source:"data/matrixsensor-disp-pic.png"
            size_hint:(0.45,0.45)
            pos:(70,130)
        
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='down'
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
        
        Button:
            background_normal:"data/sbegin-test-image.png"
            background_down:"data/sbegin-test-image-down.png"
            size_hint:(0.25,0.25)
            pos:(465,100)
            border:(0,0,0,0)
            on_release:
                root.manager.current = 'matrixscreentests1'
                root.manager.transition.direction='up'
        
        """)

#Here are coded the actual tests that will prompt the user to do things
#so that the test can proceed. 

#ECG SCREENS       
Builder.load_string("""
           
#: import Clock kivy.clock
                    
<ECGScreenTestS1>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/ecg-electrode.PNG"
            size_hint:(0.75,0.75)
            pos:(-50,40)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"This is the ECG Test. \\n Please find in the kit the \\n provided ECG electrodes as is \\n shown in the image to the left. \\n To proceed, please select \\'Next\\'."
            font_name:"CL1960"
            font_size:20
            pos:(210,50)
            
        Button:
            background_normal:"data/next-button.png"
            background_down:"data/next-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,50)
            on_release:
                root.manager.current = 'ecgscreentests2'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,50)
            on_release:
                root.manager.current = 'ecgscreen'
                root.manager.transition.direction = 'down'

<ECGScreenTestS2>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/ecg-connecter.png"
            size_hint:(0.75,0.75)
            pos:(-50,40)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"Please find in the kit the \\n provided ECG connecters as is \\n shown in the image to the left. \\n Push three ECG electrode pads \\n into the three round pin heads \\n at the end of the cable. \\n Connect the black jack connecter \\n into the DAK. \\n To proceed, select \\'Next\\'."
            font_name:"CL1960"
            font_size:20
            pos:(220,10)
            
        Button:
            background_normal:"data/next-button.png"
            background_down:"data/next-button-down.png"
            size_hint:(0.18,0.20)
            pos:(590,35)
            on_release:
                root.manager.current = 'ecgscreentests3'
                root.manager.transition.direction = 'up'
                
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.20)
            pos:(470,35)
            on_release:
                root.manager.current = 'ecgscreentests1'
                root.manager.transition.direction = 'down'
                   
<ECGScreenTestS3>


    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/ecg-sensor-placements-2.png"
            size_hint:(0.75,0.75)
            pos:(-50,20)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
        
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.20)
            pos:(480,15)
            on_release:
                root.manager.current = 'ecgscreentests2'
                root.manager.transition.direction = 'down'
                
        Button:
            background_normal:"data/start-test-button.png"
            background_down:"data/start-test-button-down.png"
            size_hint:(0.18,0.20)
            pos:(590,15)
            on_release:
                root.manager.current = 'runningtestscreenecg'
                root.manager.transition.direction = 'up'
            
        Label:
            text:"Place the white electrode pads \\n on your body according to the \\n colors of the cable heads and \\n as is shown on the diagram on \\n the left. Calm your breathing \\n and sit in one place quietly \\n and still. Select \\'Start Test\\' and \\n let the DAK run the ECG test. \\n The screen will update once \\n the test is complete."
            font_name:"CL1960"
            font_size:(20)
            pos:(220,0)
        
<RunningTestScreenECG>

    on_enter:
        root.show_results()
        root._ecg()

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/loading-gif.gif"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Label:
            text:"Please wait while the DAK runs the test."
            font_name:"CL1960"
            font_size:26
            pos:(0,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
    
        
            
<ResultScreenECG>
    
    on_enter:
        root.plot_ecg()
    
    FloatLayout:
        id: destination
        size: root.width, root.height
        
        Label:
            text:"Electrocardiogram Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Label:
            text:"Please wait while the DAK runs the test."
            font_name:"CL1960"
            font_size:26
            pos:(0,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='up'

            
                   """)

#HEART RATE AND SPO2 SCREENS                   
Builder.load_string("""
         
#: import Clock kivy.clock           
         
<HRSPO2ScreenTestS1>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Heartrate & SPO2 Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        #Image:
        #    source:"data\\ecg-electrode.png"
        #    size_hint:(0.75,0.75)
        #    pos:(-50,40)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"This is the Heartrate-SPO2 Test. \\n Please find in the kit the spot \\n marked with a heart symbol\\n as is shown in the image to the \\n left. \\n To proceed, please select \\'Next\\'."
            font_name:"CL1960"
            font_size:20
            pos:(210,40)
            
        Button:
            background_normal:"data/next-button.png"
            background_down:"data/next-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,50)
            on_release:
                root.manager.current = 'hrspo2screentests2'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,50)
            on_release:
                root.manager.current = 'hrspo2screen'
                root.manager.transition.direction = 'down'
                
<HRSPO2ScreenTestS2>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Heartrate & SPO2 Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        #Image:
        #    source:"data\\ecg-electrode.png"
        #    size_hint:(0.75,0.75)
        #    pos:(-50,40)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"Please place your finger on the \\n glass film where heart symbol \\n is marked. Make sure your finger \\n is in the centre and is firmly \\n pressed down. Do not move your \\n finger while the test is \\n in progress. \\n Select \\'Start Test\\' when your are \\n ready."
            font_name:"CL1960"
            font_size:20
            pos:(210,10)
            
        Button:
            background_normal:"data/start-test-button.png"
            background_down:"data/start-test-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,20)
            on_release:
                root.manager.current = 'runningtestscreenhrspo2'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,20)
            on_release:
                root.manager.current = 'hrspo2screentests1'
                root.manager.transition.direction = 'down'
                    
<RunningTestScreenHRSPO2>

    on_enter:
        root.show_results()
        root._hrspo2()
        
    on_leave:
        root.set_text()

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Heartrate and SPO2 Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/loading-gif.gif"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Label:
            text:"Please wait while the DAK runs the test."
            font_name:"CL1960"
            font_size:26
            pos:(0,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
                    
<ResultScreenHRSPO2>
    
    #on_enter:
        #root.plot_ecg()
        #root.show_results()
        #root._hrspo2()
    
    FloatLayout:
        #id: destination
        size: root.width, root.height
        
        Label:
            text:"Heartrate and SPO2 Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Label:
            text:"SPO2"
            font_name:"CNY1960"
            font_size:24
            pos:(-60,-120)
            
        Label:
            text:"Heart\\n rate"
            font_name:"CNY1960"
            font_size:24
            pos:(65,-130)
            
        Label:
            text: root.avg_spo2
            font_name:"CL1960"
            font_size:26
            pos:(-60,-90)
            
        Label:
            text: root.avg_hr
            font_name:"CL1960"
            font_size:26
            pos:(60,-90)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        #Label:
        #    text:"Please wait while the DAK runs the test."
        #    font_name:"CL1960"
        #    font_size:26
        #    pos:(0,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='up'
                    
                    """)

#TEMPERATURE SCREENS
Builder.load_string("""
                    
<TEMPScreenTestS1>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Temperature Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/temp-sensor.png"
            size_hint:(0.5,0.5)
            pos:(20,100)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"This is the Temperature Test. \\n Please find in the kit the \\n provided temperature probe as is \\n shown in the image to the left. \\n To proceed, please select \\'Next\\'."
            font_name:"CL1960"
            font_size:20
            pos:(210,50)
            
        Button:
            background_normal:"data/next-button.png"
            background_down:"data/next-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,50)
            on_release:
                root.manager.current = 'tempscreentests2'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,50)
            on_release:
                root.manager.current = 'tempscreen'
                root.manager.transition.direction = 'down'
                    
                
<TEMPScreenTestS2>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Temperature Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/temp-sensor.png"
            size_hint:(0.5,0.5)
            pos:(20,100)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"Place the metallic end of the \\n probe on the opposite side \\n of your elbow (the \\n chelidon) and fold your elbow. \\n You may also place it under \\n your armpit and fold your arm. \\n Select \\'Start Test\\' when ready."
            font_name:"CL1960"
            font_size:20
            pos:(200,30)
            
        Button:
            background_normal:"data/start-test-button.png"
            background_down:"data/start-test-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,50)
            on_release:
                root.manager.current = 'runningtestscreentemp'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,50)
            on_release:
                root.manager.current = 'tempscreentests1'
                root.manager.transition.direction = 'down'

<RunningTestScreenTEMP>

    on_enter:
        root.show_results()
        root._temp()
        #root.start_thread()
    on_leave:
        root.set_text()

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Temperature Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Label:
            text:"Please wait while the DAK runs the test."
            font_name:"CL1960"
            font_size:26
            pos:(0,-90)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/loading-gif.gif"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()

<ResultScreenTEMP>
    
    #on_enter:
    #    root.show_temp()
    
    FloatLayout:
        #id: destination
        size: root.width, root.height
        
        Label:
            text:"Temperature Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
        
        Label:
            text:"  Maximum\\nTemperature"
            font_name:"CNY1960"
            font_size:24
            pos:(-80,-130)
            
        Label:
            text:"  Average\\nTemperature"
            font_name:"CNY1960"
            font_size:24
            pos:(90,-130)
        
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        #Label:
        #    text:"Please wait while the DAK runs the test."
        #   font_name:"CL1960"
        #    font_size:26
        #    pos:(0,-90)
            
        Label:
            text: root.max_temp
            font_name:"CL1960"
            font_size:26
            pos:(-80,-90)
            
        Label:
            text: root.avg_temp
            font_name:"CL1960"
            font_size:26
            pos:(80,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='up'

                    """)

#MATRIX SCREENS
Builder.load_string("""
                    
<MATRIXScreenTestS1>

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Matrix Sensor Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Image:
            source:"data/matrix-sensor-disp-pic.png"
            size_hint:(0.5,0.5)
            pos:(20,100)
            
        Image:
            source:"data/instructions-outline.png"
            size_hint:(0.6,0.8)
            pos:(365,10)
            
        Label:
            text:"This is the Matrix Sensor Test. \\n [STILL EXPERIMENTAL] \\n Place your hand or an object \\n on the sensor to see a \\n pressure map. \\n To proceed, please select \\'Next\\'."
            font_name:"CL1960"
            font_size:20
            pos:(210,50)
            
        Button:
            background_normal:"data/next-button.png"
            background_down:"data/next-button-down.png"
            size_hint:(0.18,0.20)
            pos:(600,50)
            on_release:
                root.manager.current = 'runningtestscreenmatrix'
                root.manager.transition.direction = 'up'          
        Button:
            background_normal:"data/back-button.png"
            background_down:"data/back-button-down.png"
            size_hint:(0.18,0.205)
            pos:(470,50)
            on_release:
                root.manager.current = 'matrixscreen'
                root.manager.transition.direction = 'down'

<RunningTestScreenMATRIX>

    on_enter:
        root.show_results()
        #root._temp()
        #root.start_thread()

    FloatLayout:
        size: root.width, root.height
        
        Label:
            text:"Matrix Sensor Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Label:
            text:"Please wait while the DAK runs the test."
            font_name:"CL1960"
            font_size:26
            pos:(0,-90)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/loading-gif.gif"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()

<ResultScreenMATRIX>
    
    on_enter:
        root.matrix()
    
    FloatLayout:
        #id: destination
        size: root.width, root.height
        
        Label:
            text:"Matrix Sensor Test"
            font_name:"CNY1960"
            font_size:30
            pos:(0,155)
            bold:True
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.2,0.2)
            pos:(-35,315)
            
        Image:
            source:"data/heart-health.png"
            size_hint:(0.4,0.4)
            pos:(250,140)
            
        Label:
            id: max_temp
            #text:root.displaying_temp_max()
            font_name:"CL1960"
            font_size:26
            pos:(-30,-90)
            
        Label:
            id: avg_temp
            #text:root.displaying_temp_avg()
            font_name:"CL1960"
            font_size:26
            pos:(30,-90)
            
        Button:
            background_normal:"data/cross-button-b.png"
            size_hint:(0.05,0.08)
            pos:(750,360)
            border:(0,0,0,0)
            on_release:root.killapp()
            
        Button:
            background_normal:"data/home-button.png"
            background_down:"data/home-button-down.png"
            size_hint:(0.09,0.18)
            pos:(700,5)
            border: (0,0,0,0)
            on_release:
                root.manager.current = 'homescreen'
                root.manager.transition.direction='up'

                    """)

class WelcomeScreen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        pass

class HomeScreen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class ECGScreen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class ECGScreenTestS1(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class ECGScreenTestS2(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class ECGScreenTestS3(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()

#Helper function
#def result_ecg(dt):
#    global sm, _result_ecg
#    sm.current = 'resultscreenecg'
#    sm.add_widget(RunningTestScreenECG(name='runningtestscreen'))
class RunningTestScreenECG(Screen):
#Runs the ECG test and then sends the data to our google sheet    
    def killapp(instance):
        App.get_running_app().stop()
        
    def _ecg(instance):
        global ecg_data
        ecg_data = ecg.get_ecg()
        data = wks.range('B2:B1000')
        
        for i, val in enumerate(ecg_data):
            data[i].value = val
            
        wks.update_cells(data)
         
    def results(self,dt):
        global sm
        sm.current='resultscreenecg'
        
    def show_results(self):
        global sm
        Clock.schedule_once(self.results,60)
        #Clock.schedule_once(result_ecg,10)
         
class ResultScreenECG(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
    def plot_ecg(self):
        global ecg_data
        start = random.randint(200,699)
        y_data = []
        for i in range(300):
            y_data.append(ecg_data[start+i])
        y_data = np.array(y_data)
        plt.plot(y_data)
        plt.xlabel('Time(s)')
        plt.ylabel('ECG Graph')
        plt.grid(True, color='lightgray')
        plt.rcParams['figure.figsize'] = (20,3)
        #f = plt.figure()
        #f.set_figwidth(0.5)
        #f.set_figheight(0.2)
        self.manager.get_screen('resultscreenecg').ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        y_data = []
        #layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #return ResultScreenECG.str
        

class HRSPO2Screen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class HRSPO2ScreenTestS1(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class HRSPO2ScreenTestS2(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()

class RunningTestScreenHRSPO2(Screen):
#Runs the ECG test and then sends the data to our google sheet    
    def killapp(instance):
        App.get_running_app().stop()
        
    def _hrspo2(instance):
        global hr_data, spo2_data
        hr_data, spo2_data = hrspo2.get_hrspo2()
        data1 = wks.range('D2:D201')
        data2 = wks.range('C2:C201')
        
        for i, val in enumerate(hr_data):
            data1[i].value = val
            
        for i, val in enumerate(spo2_data):
            data2[i].value = val
            
        wks.update_cells(data1)
        wks.update_cells(data2)
         
    def results(self,dt):
        global sm
        sm.current='resultscreenhrspo2'
        
    def show_results(self):
        global sm
        Clock.schedule_once(self.results,60)
        #Clock.schedule_once(result_ecg,10)
    def set_text(self):
        global hr_data, spo2_data
        _spo2_data = []
        _hr_data = []
        for count in range(49):
            _spo2_data.append(spo2_data[len(spo2_data)-(count+49)-1])
            _hr_data.append(hr_data[len(hr_data)-(count+49)-1])
        
        _avg_spo2 = np.mean(_spo2_data)
        _avg_spo2 = '{0:.3g}'.format(_avg_spo2)
        #_max_temp = str(max(temp_data))
        _avg_hr = np.mean(_hr_data)
        _avg_hr = '{0:.3g}'.format(_avg_hr)
        #_avg_temp = str(np.mean(temp_data))
        self.manager.get_screen('resultscreenhrspo2').avg_spo2 = _avg_spo2
        self.manager.get_screen('resultscreenhrspo2').avg_hr = _avg_hr
        
class ResultScreenHRSPO2(Screen):
    avg_spo2 = StringProperty('Hello')
    avg_hr = StringProperty('Hey')
    
    def killapp(instance):
        App.get_running_app().stop()

class TempScreen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class TempScreenTestS1(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class TempScreenTestS2(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()

class RunningTestScreenTEMP(Screen):
    global temp_data
    temp_data = []
    
    
    def killapp(instance):
        App.get_running_app().stop()
        
    def _temp(instance):
        global temp_data
        #file = open('displayvalues.txt')
        #d = file.readlines()
        #file.close()
        
        temp_data = []
        temp_data = temp.get_temp()
        for value in temp_data:
            value = float('{0:.3g}'.format(value))
            print(str(value))
        data = wks.range('E2:E41')
        
        for i, val in enumerate(temp_data):
            data[i].value = val
        
        wks.update_cells(data)
        time.sleep(2)
        
    def start_thread(instance):
        t = threading.Thread(target=RunningTestScreenTEMP._temp)
        t.start()
        t.join()
         
    def results(self,dt):
        global sm
        sm.current='resultscreentemp'
        
    def show_results(self):
        global sm
        Clock.schedule_once(self.results,60)
        #Clock.schedule_once(result_ecg,10)
        
    def set_text(self):
        global temp_data
        _max_temp = max(temp_data)
        _max_temp = '{0:.3g}'.format(_max_temp)
        #_max_temp = str(max(temp_data))
        _avg_temp = np.mean(temp_data)
        _avg_temp = '{0:.3g}'.format(_avg_temp)
        #_avg_temp = str(np.mean(temp_data))
        self.manager.get_screen('resultscreentemp').max_temp = _max_temp
        self.manager.get_screen('resultscreentemp').avg_temp = _avg_temp


class ResultScreenTEMP(Screen):
    max_temp = StringProperty('Hello')
    avg_temp = StringProperty('Hey')
    
    def killapp(instance):
        App.get_running_app().stop()
        
class MatrixScreen(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class MATRIXScreenTestS1(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
class RunningTestScreenMATRIX(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
    def results(self,dt):
        global sm
        sm.current='resultscreenmatrix'
        
    def show_results(self):
        global sm
        Clock.schedule_once(self.results,5)
        #Clock.schedule_once(result_ecg,10)
        
class ResultScreenMATRIX(Screen):
    
    def killapp(instance):
        App.get_running_app().stop()
        
    def matrix(instance):
        matrixsensor.matrixsensor()

class myApp(App):
    def build(self):
        global sm, _result_ecg
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcomescreen'))
        sm.add_widget(HomeScreen(name='homescreen'))
        sm.add_widget(ECGScreen(name='ecgscreen'))
        sm.add_widget(HRSPO2Screen(name='hrspo2screen'))
        sm.add_widget(TempScreen(name='tempscreen'))
        sm.add_widget(MatrixScreen(name='matrixscreen'))
        
        sm.add_widget(ECGScreenTestS1(name='ecgscreentests1'))
        sm.add_widget(ECGScreenTestS2(name='ecgscreentests2'))
        sm.add_widget(ECGScreenTestS3(name='ecgscreentests3'))
        sm.add_widget(RunningTestScreenECG(name='runningtestscreenecg'))
        _result_ecg = ResultScreenECG(name='resultscreenecg')
        sm.add_widget(_result_ecg)
        
        sm.add_widget(HRSPO2ScreenTestS1(name='hrspo2screentests1'))
        sm.add_widget(HRSPO2ScreenTestS2(name='hrspo2screentests2'))
        sm.add_widget(RunningTestScreenHRSPO2(name='runningtestscreenhrspo2'))
        sm.add_widget(ResultScreenHRSPO2(name='resultscreenhrspo2'))
        
        sm.add_widget(TempScreenTestS1(name='tempscreentests1'))
        sm.add_widget(TempScreenTestS2(name='tempscreentests2'))
        sm.add_widget(RunningTestScreenTEMP(name='runningtestscreentemp'))
        sm.add_widget(ResultScreenTEMP(name='resultscreentemp'))
        
        sm.add_widget(MATRIXScreenTestS1(name='matrixscreentests1'))
        sm.add_widget(RunningTestScreenMATRIX(name='runningtestscreenmatrix'))
        sm.add_widget(ResultScreenMATRIX(name='resultscreenmatrix'))
        return sm
    
    def refresh(self,ins):
        self.sm.refresh()
    
if __name__ == '__main__':
    myApp().run()
