'''
Created on Sep 24, 2016

@author: Loaner
'''

from Comm import CommWithArduino
import time

CAR_PORT_NUMBER = 7
MUSCLE_PORT_NUMBER = 8
THRESHOLD = 512 
WINDOW = 32
leftcount = 0
rightcount = 0
leftstate = False
rightstate = False

if __name__ == '__main__':
    
    print("Muscle Test Application for Car Control.")
    
    print("Attempting to connect to devices.")
    
    with CommWithArduino( CAR_PORT_NUMBER ) as car, \
            CommWithArduino( MUSCLE_PORT_NUMBER, 76800 ) as mus:
        
        raw_input("Hit enter to start application.")
        
        while True:
            
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
                
                print("left: " + repr(leftstate) + ", right: " + repr(rightstate))
                left = 1.0 if leftstate==True else -1.0
                right = 1.0 if rightstate==True else -1.0
                car.setMotors(left,right)
            pass
            
        pass