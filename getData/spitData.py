import sys
import os
import platform
import time
import math
import matplotlib.pyplot as plt
from array import *
from ctypes import *
from __builtin__ import exit

class spitData:
    """This class makes Andrew happy because its the right way to code """
    
    def __init__(self):
        if sys.platform.startswith('win32'):
                import msvcrt
        elif sys.platform.startswith('linux'):
                import atexit
                from select import select
                
        try:
            if sys.platform.startswith('win32'):
                self.libEDK = cdll.LoadLibrary("bin/win64/edk.dll")
            elif sys.platform.startswith('linux'):
                srcDir = os.getcwd()
                if platform.machine().startswith('arm'):
                    self.libPath = srcDir + "bin/armhf/libedk.so"
                else:
                    self.libPath = srcDir + "bin/linux64/libedk.so"
                self.libEDK = CDLL(self.libPath)
            else:
                raise Exception('System not supported.')
        except Exception as e:
            print 'Error: cannot load EDK lib:', e
            exit()
            
        self.userID = c_uint(0)
        self.user   = pointer(self.userID)
        self.ready  = 0
        self.state  = c_int(0)

        self.alphaValue     = c_double(0)
        self.low_betaValue  = c_double(0)
        self.high_betaValue = c_double(0)
        self.gammaValue     = c_double(0)
        self.thetaValue     = c_double(0)

        self.alpha     = pointer(self.alphaValue)
        self.low_beta  = pointer(self.low_betaValue)
        self.high_beta = pointer(self.high_betaValue)
        self.gamma     = pointer(self.gammaValue)
        self.theta     = pointer(self.thetaValue)

        self.channelList = array('I',[3, 7, 9, 12, 16])   # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz 
            
    def openConnection(self):
        IEE_EmoEngineEventCreate = self.libEDK.IEE_EmoEngineEventCreate
        IEE_EmoEngineEventCreate.restype = c_void_p
        self.eEvent = IEE_EmoEngineEventCreate()

        IEE_EmoEngineEventGetEmoState = self.libEDK.IEE_EmoEngineEventGetEmoState
        IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
        IEE_EmoEngineEventGetEmoState.restype = c_int

        IEE_EmoStateCreate = self.libEDK.IEE_EmoStateCreate
        IEE_EmoStateCreate.restype = c_void_p
        self.eState = IEE_EmoStateCreate()

        if self.libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
            print "Emotiv Engine start up failed."
            exit();
        else:
            print "Emotiv Engine started up correctly"
        
        print "openConnection complete"
        
    def openFile(self,fileName):
        self.fileName = fileName
        self.header = "Channel, Theta, Alpha, Low_beta, High_beta, Gamma \n"
        self.f = file(self.fileName,'w')
        self.f = open(self.fileName,'w')
        print >> self.f, self.header
        
    def closeFile(self):
        self.f.close()
        
    def writePlot(self):
        plt.ion()
        self.ln, = plt.plot([])
        
        if( (len(self.plotArray) % 5) == 0 ):
            plt.gcf().clear()
            zulu = plt.plot(self.plotArray[-40:])
            plt.legend(zulu,('theta','alpha','lowB','highB','gamma'))
            plt.pause(0.001)
            print "plot now"  
    
    def linkUser(self):        
        ready = 0
        self.state = self.libEDK.IEE_EngineGetNextEvent(self.eEvent)
        if self.state == 0:
            eventType = self.libEDK.IEE_EmoEngineEventGetType(self.eEvent)
            self.libEDK.IEE_EmoEngineEventGetUserId(self.eEvent, self.user)
            if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
                ready = 1
                self.libEDK.IEE_FFTSetWindowingType(self.userID, 1);  # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
                print "User added"
        elif self.state != 0x0600:
                print "Internal error in Emotiv Engine ! "
        return ready
                
    def collectData(self,channel):
        self.plotArray = []
        channelMap = {3:0,7:1,9:2,12:3,16:4}
        #p rint "channel target: %d" % (channel)                
        for i in self.channelList: 
            result = c_int(0)
            result = self.libEDK.IEE_GetAverageBandPowers(self.userID, i, self.theta, self.alpha, self.low_beta, self.high_beta, self.gamma)
            # print "channel loop: %d" % (i)
            # print "lib result: %d" % (result)
            if result == 0:    #EDK_OK
                # print "%d, %.6f, %.6f, %.6f, %.6f, %.6f \n" % (i, self.thetaValue.value, self.alphaValue.value, 
                #                                               self.low_betaValue.value, self.high_betaValue.value, self.gammaValue.value)
                # print >> self.f, "%d, %.6f, %.6f, %.6f, %.6f, %.6f" % (i, self.thetaValue.value, self.alphaValue.value, 
                #                                                          self.low_betaValue.value, self.high_betaValue.value, self.gammaValue.value)
                if i == channel:
                    # print "channel match"
                    self.plotArray.append([math.log10(self.thetaValue.value),math.log10(self.alphaValue.value),math.log10(self.low_betaValue.value),
                                              math.log10(self.high_betaValue.value),math.log10(self.gammaValue.value)])       
                    print str(self.plotArray[-10:]).strip('[]')
                    return self.plotArray[channelMap[i]]
        
    def closeConnection(self):
        self.libEDK.IEE_EngineDisconnect()
        self.libEDK.IEE_EmoStateFree(self.eState)
        self.libEDK.IEE_EmoEngineEventFree(self.eEvent)
        
    def channelBand(self,channel,band):
        data = self.collectData(channel)
        if not data:
            print 'data is empty in channelBand'
            return -1
        else:
            # print 'band value: %d' % (band)
            chosenData = data[band-1]
            return(chosenData)