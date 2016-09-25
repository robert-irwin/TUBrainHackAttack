'''
Created on Sep 23, 2016
'''

from Comm import CommWithArduino
import msvcrt

PORT_NUMBER = 7
END_VAL = 'q'
LEFT_VAL = 'a'
RIGHT_VAL = 'd'
FORWARD_VAL = 'w'
BACKWARD_VAL = 's'

if __name__ == '__main__':
    
    print( "Starting test application." )
    
    data = bytearray([3,2])
    
    with CommWithArduino( PORT_NUMBER ) as com:
        
        print("Connection established.")
        raw_input("Hit enter to continue.")
        com.setMotors(0.0,0.0)
        print("Program started.")
        val = msvcrt.getch()
        while val!=END_VAL:
            print(val)
            if (val==LEFT_VAL):
                print("left")
                com.setMotors(-1.0,1.0)
                pass
            elif (val==RIGHT_VAL):
                print("right")
                com.setMotors(1.0,-1.0)
                pass
            elif (val==FORWARD_VAL):
                print("forward")
                com.setMotors(1.0,1.0)
                pass
            elif (val==BACKWARD_VAL):
                print("stop")
                com.setMotors(0.0,0.0)
                pass
            
            val = msvcrt.getch()
        
        
        
        
        raw_input("Hit enter to continue.")
        pass
    pass

    print( "Testing application has finished.")