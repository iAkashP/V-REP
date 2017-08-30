#V-REP
#Wrapper Creation for importing sensor data with threading support
#written with Pioneer_p3dx bot

import sys
import time
import threading
from random import randint
from getch import getch, pause
import xlwt                       #for dumping sensor data in .xls file
import numpy as np
import matplotlib.pyplot as plt
import vrep                       #importing v-rep module


class RanW(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval =5


    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        while 1:
            if self._finished.isSet(): return
            self.task()

            # sleep for interval or until shutdown
            self._finished.wait(self._interval)

    def task(self):
	coll_dist=0.2
	ObstAvoid(coll_dist)
	pass

    def ReadSensor(botnum,sensornum):
    frt=((botnum-1)*mp.sensor_count)+(sensornum-1)
    current_sensor_handle=mp.sensor_handle[frt]
    returnCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,current_sensor_handle,vrep.simx_opmode_streaming)
    time.sleep(0.01)
    returnCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,current_sensor_handle,vrep.simx_opmode_buffer)
    distance=detectedPoint[2]
    if (distance<0.00001):
        distance=(np.random.rand()/10)+0.9
    if (distance>1):
        distance=1
    return distance
	
    def SetMotor():
	#to-do

    def ObstAvoid(coll_dist):
    SetMotor(1,0,0)
    leftsensor=(ReadSensor(1,2)+ReadSensor(1,3))/2
    frontsensor=(ReadSensor(1,4)+ReadSensor(1,5))/2
    rightsensor=(ReadSensor(1,6)+ReadSensor(1,7))/2
    print(leftsensor,frontsensor,rightsensor)
    
    if(frontsensor<coll_dist):
        SetMotor(1,-0.2,-0.2)
        time.sleep(1)
        SetMotor(1,0.2,-0.2)
    elif(leftsensor<coll_dist):
        SetMotor(1,0.4,-0.4)
    elif(rightsensor<coll_dist):
        SetMotor(1,-0.4,0.4)
    elif(rightsensor>coll_dist and leftsensor>coll_dist):
        SetMotor(1,1,1)
    time.sleep(0.5)

    def MoveBot(chart,Reg,io_count,velocity):
    motor_code=0
    perturbation=np.random.rand()/10
    effect=np.random.rand()
    if effect<0.5:
        velocity=velocity-perturbation
    else:
        velocity=velocity+perturbation

    if (chart=='w'):
        SetMotor(1,velocity,velocity)
        motor_code=0.5                       #assigning value or char(motor_code)
    if (chart=='a'):
        SetMotor(1,-velocity,velocity)
        motor_code=0.25
    if (chart=='s'):
        SetMotor(1,-velocity,-velocity)
        motor_code=1
    if (chart=='d'):
        SetMotor(1,velocity,-velocity)
        motor_code=0.75
    if (chart==' '):
        Reg.save('Regression_file.xls')
        sys.exit()
    time.sleep(0.1)
    leftsensor=(ReadSensor(1,2)+ReadSensor(1,3))/2
    frontsensor=(ReadSensor(1,4)+ReadSensor(1,5))/2
    rightsensor=(ReadSensor(1,6)+ReadSensor(1,7))/2

    Reg_sheet.write(io_count,0,chart)
    Reg_sheet.write(io_count,2,motor_code)
    Reg_sheet.write(io_count,3,leftsensor)
    Reg_sheet.write(io_count,4,frontsensor)
    Reg_sheet.write(io_count,5,rightsensor)
    return leftsensor,frontsensor,rightsensor

RanW().start()                               #calling thread

Reg = xlwt.Workbook()
Reg_sheet = Reg.add_sheet('Regression_sheet',cell_overwrite_ok=True)
Reg_sheet.write(0,0,'Char')
Reg_sheet.write(0,2,'motor_code')
Reg_sheet.write(0,3,'LEFT SENSOR')
Reg_sheet.write(0,4,'FRONT SENSOR')
Reg_sheet.write(0,5,'RIGHT SENSOR')
tt=0
while(1):
    time.sleep(0.1)
    SetMotor(1,0,0)
    chart=getch()
    tt=tt+1
    leftsensor,frontsensor,rightsensor=MovBot(chart,Reg,tt,1)
