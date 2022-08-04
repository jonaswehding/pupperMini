# This is a sample Python script.
import time
import serial as ser
import numpy as np
import math
import sys
from typing import List
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#from dataclasses import dataclass, field

s = ser.Serial(port="/dev/ttyS0",baudrate=230400)
mapSize = 60

map = np.empty((mapSize,mapSize),dtype=int)

def plot(x,y,char):
    global map
    map[int(x+(mapSize/2))][int((mapSize/2)-y)] = char

def clear():
    global map
    #map = np.zeros((mapSize,mapSize),dtype=int)
    map = np.full((mapSize,mapSize),32)


def mapshow():
    global map
    print("\033c")
    for y in range(mapSize):
        for x in range(mapSize):
            print(chr(map[x][y])+' ', end='')
        print('')




def getCoord(angle,dist):
    x =(dist*(np.sin(math.radians(angle))))
    y =(dist*(np.cos(math.radians(angle))))
    return x/100,y/100



def getFrame():

    data = np.empty((0, 3), float)
    totalAngle=0
    angles = []
    distances = []
    while True:

            

            d=s.read(2)
            while d[0]!=54 and d[1]!=0x2C:
                d = s.read(2)
            # if header and ver_len
            fr = s.read(45)
            frameList = list(fr)
            startAngle = (frameList[2])+(frameList[3]<<8)
            endAngle = (frameList[40])+(frameList[41]<<8)
            timeStamp = (frameList[42])+(frameList[43]<<8)

            diff = (endAngle + 36000 - startAngle) % 36000
            step = diff / (12 - 1) / 100.0
            start = startAngle / 100.0
            end = (endAngle % 36000) / 100.0

            totalAngle += step*12
            #print(totalAngle)
            
            if totalAngle>=360:
                totalAngle=0
                return angles,distances#data
                
            byteOffset = 0

            for i in range(12):


                byte1=frameList[4+byteOffset]
                byte2=frameList[4+byteOffset+1]
                conf = frameList[4+byteOffset+2]

                #x_,y_= getCoord((start+(step*i)),(byte1+(byte2<<8)))
                angle = (start+((step)*i))
                distance = (byte1+(byte2<<8))
           
                #print(x_,y_,conf)
              
                #print (angle)
                angles.append(angle)
                distances.append(distance)
                #data = np.append(data,np.array([[angle,distance,conf]]), axis = 0)
                
                byteOffset+=3

#while 1:
#
#    dat = getFrame()
#    clear()
#    plot(0,0,ord('O'))
#    for point in dat:
#        angle = point[0]
#        distance = point[1]
#        x,y = getCoord(angle,distance)
#
#        #print(angle,distance,x,y)
#        conf = int(point[2])
#        if conf>220:
#             plot(x,y,ord('#'))
#        #print(x,y)
#
#        #col = int(point[2])
#        #print(angle,distance,col)
#
#    mapshow()
#    #time.sleep(0.01)
#    #s.flushInput()



