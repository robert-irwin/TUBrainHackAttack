'''
Created on Sep 23, 2016

@author: Loaner
'''

import serial

class CommWithArduino(object):
    
    BAUD_RATE = 9600
    MAX_SIZE = 8
    CONTROL_SIZE = 3;
    START_BYTE = 12
    START_LOC = 0
    SIZE_LOC = 1
    END_BYTE = 52
    
    PAYLOAD_ID_LOC = 0
    
    MOTORS_ID = 0
    MOTORS_OUT_MIN = 64
    MOTORS_OUT_MAX = 128
    MOTORS_IN_MIN = -1
    MOTORS_IN_MAX = 1
    MOTORS_LEFT_DIR = 1
    MOTORS_RIGHT_DIR = 1
    MOTORS_MAP_M = (MOTORS_OUT_MAX-MOTORS_OUT_MIN)/(MOTORS_IN_MAX-MOTORS_IN_MIN)
    MOTORS_MAP_C = MOTORS_OUT_MIN-MOTORS_MAP_M*MOTORS_IN_MIN

    def __init__(self,comport):
        
        assert(isinstance(comport,int))
        
        self.ser = serial.Serial(port='COM' + repr(comport),
             baudrate=CommWithArduino.BAUD_RATE,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             timeout=None)
        
    def send(self,data):
        
        assert(isinstance(data,bytearray))
        size = CommWithArduino.CONTROL_SIZE+len(data)
        assert(size<=CommWithArduino.MAX_SIZE)
        packet = bytearray()
        packet.append(CommWithArduino.START_BYTE)
        packet.append(size)
        for b in data: packet.append(b)
        packet.append(CommWithArduino.END_BYTE)
        self.ser.write(packet)
        
    def setMotors(self,left,right):
        
        assert(isinstance(left,float))
        assert(isinstance(right,float))
        assert((left>=-1.0)and(left<=1.0))
        assert((right>=-1.0)and(right<=1.0))
        
        left *= CommWithArduino.MOTORS_LEFT_DIR
        right *= CommWithArduino.MOTORS_RIGHT_DIR
        m = CommWithArduino.MOTORS_MAP_M
        c = CommWithArduino.MOTORS_MAP_C
        left = int(left*m+c)
        right = int(right*m+c)
        
        payload = bytearray()
        payload.append(CommWithArduino.MOTORS_ID)
        payload.append(left)
        payload.append(right)
        
        self.send(payload)
        
    def __del__(self):
        
        self.ser.close()
        
    def __enter__(self):
        
        return self
    
    def __exit__(self,type_0,value,traceback):
        self.__del__()


        