'''
Created on Sep 24, 2016

@author: Loaner
'''

from comm.Comm import CommWithArduino

PORT_NUMBER = 6

if __name__ == '__main__':
    
    print( "Starting test application." )
    
    with CommWithArduino( PORT_NUMBER, 115200 ) as com:
        
        raw_input("Hit enter to continue.")
        while True:
            data = com.getMuscles()
            if data!=None:
                (left,right) = data
                print(left)
                print(right)
                
                
            pass
        print("Finished.")
    pass