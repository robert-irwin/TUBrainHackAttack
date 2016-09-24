import sys
import os
import platform
import time
import math
import matplotlib.pyplot as plt
import ctypes

if sys.platform.startswith('win32'):
    import msvcrt
elif sys.platform.startswith('linux'):
    import atexit
    from select import select

from array import *
from ctypes import *
from __builtin__ import exit

try:
    if sys.platform.startswith('win32'):
        libEDK = cdll.LoadLibrary("bin/win64/edk.dll")
    elif sys.platform.startswith('linux'):
        srcDir = os.getcwd()
	if platform.machine().startswith('arm'):
            libPath = srcDir + "bin/armhf/libedk.so"
	else:
            libPath = srcDir + "bin/linux64/libedk.so"
        libEDK = CDLL(libPath)
    else:
        raise Exception('System not supported.')
except Exception as e:
    print 'Error: cannot load EDK lib:', e
    exit()

IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()

IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int

IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()

userID = c_uint(0)
user   = pointer(userID)
ready  = 0
state  = c_int(0)

alphaValue     = c_double(0)
low_betaValue  = c_double(0)
high_betaValue = c_double(0)
gammaValue     = c_double(0)
thetaValue     = c_double(0)

alpha     = pointer(alphaValue)
low_beta  = pointer(low_betaValue)
high_beta = pointer(high_betaValue)
gamma     = pointer(gammaValue)
theta     = pointer(thetaValue)

channelList = array('I',[3, 7, 9, 12, 16])   # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz 

# -------------------------------------------------------------------------
print "==================================================================="
print "Example to get the average band power for a specific channel from" \
" the latest epoch."
print "==================================================================="

# -------------------------------------------------------------------------
if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
        print "Emotiv Engine start up failed."
        exit();

header = "Channel, Theta, Alpha, Low_beta, High_beta, Gamma \n"
# print header

f = file('spitData.csv','w')
f = open('spitData.csv','w')

plt.ion()
ln, = plt.plot([])
plotArray = []
print >> f, header

while (1):
    
    state = libEDK.IEE_EngineGetNextEvent(eEvent)
    
    if state == 0:
        eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
        libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
        if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
            ready = 1
            libEDK.IEE_FFTSetWindowingType(userID, 1);  # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
            print "User added"
                        
        if ready == 1:
            for i in channelList: 
                result = c_int(0)
                result = libEDK.IEE_GetAverageBandPowers(userID, i, theta, alpha, low_beta, high_beta, gamma)
    
                if result == 0:    #EDK_OK
                   #  print "%d, %.6f, %.6f, %.6f, %.6f, %.6f \n" % (i, thetaValue.value, alphaValue.value, 
                   #     low_betaValue.value, high_betaValue.value, gammaValue.value)
                    print >> f, "%d, %.6f, %.6f, %.6f, %.6f, %.6f" % (i, thetaValue.value, alphaValue.value, 
                        low_betaValue.value, high_betaValue.value, gammaValue.value)
                    if i == 3:
                        plotArray.append([math.log10(thetaValue.value),math.log10(alphaValue.value),math.log10(low_betaValue.value),
                                          math.log10(high_betaValue.value),math.log10(gammaValue.value)])
                        if( (len(plotArray) % 5) == 0 ):
                            plt.gcf().clear()
                            zulu = plt.plot(plotArray[-40:])
                            plt.legend(zulu,('theta','alpha','lowB','highB','gamma'))
                            plt.pause(0.001)
                            print "plot now"         
                elif state != 0x0600:
                    print "Internal error in Emotiv Engine ! "
        time.sleep(0.001)
        print str(plotArray[-10:]).strip('[]')
f.close()    
# -------------------------------------------------------------------------
libEDK.IEE_EngineDisconnect()
libEDK.IEE_EmoStateFree(eState)
libEDK.IEE_EmoEngineEventFree(eEvent)