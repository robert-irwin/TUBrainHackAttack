'''
Created on Sep 24, 2016

@author: Loaner
'''

from Comm import CommWithArduino
from spitData import spitData

CAR_PORT_NUMBER = 7
MUSCLE_PORT_NUMBER = 5
EEG_CHANNEL = 12
EEG_BAND = 2
EEG_THRESHOLD = 3

THRESHOLD = 512 
WINDOW = 32

leftcount = 0
rightcount = 0
leftstate = False
rightstate = False

eegstate = False
motorstate = False


if __name__ == '__main__':
    
    print("Muscle Test Application for Car Control.")
    
    print("Attempting to connect to devices.")
    
    
    
    with CommWithArduino( CAR_PORT_NUMBER ) as car, \
            CommWithArduino( MUSCLE_PORT_NUMBER, 76800 ) as mus, \
            spitData() as zulu:
        
        raw_input("Hit enter to start application.")
        
        zulu.openConnection()
        
        link_status = -1
        
        while link_status < 1:
            link_status = zulu.linkUser()
            print "Link status: %d" % (link_status)
        
        while True:
            
            data = zulu.moveTheCar( EEG_CHANNEL, EEG_BAND )
            print("EEG Data: " + repr(data))
            
            if ((data>=EEG_THRESHOLD)and(eegstate==False)):
                eegstate = True
                motorstate = not motorstate
                
            if ((data<EEG_THRESHOLD)and(eegstate==True)):
                eegstate = False
                
            
            print("motor state:"+repr(motorstate))
            
            data = mus.getMuscles()
            if data!=None:
                (left,right) = data
                
                if left>THRESHOLD:
                    leftcount = 0
                    leftstate = True
                elif leftcount==WINDOW:
                    leftstate = False
                if right>THRESHOLD:
                    rightcount = 0
                    rightstate = True
                elif rightcount==WINDOW:
                    rightstate = False
                    
                leftcount += 1
                rightcount += 1
                    
                if leftstate==True:
                    pass
                if rightstate==True:
                    pass
                
                #print("left: " + repr(leftstate) + ", right: " + repr(rightstate))
                val = 1.0 if motorstate else 0.00000
                left = val if leftstate==True else -val
                right = val if rightstate==True else -val
                print("left: " + repr(left) + ", right: " + repr(right))
                car.setMotors(left,right)
            pass
            
        pass