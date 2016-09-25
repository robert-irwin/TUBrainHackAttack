'''
Created on Sep 24, 2016

@author: NIL
'''
import time
import spitData

zulu = spitData.spitData()

channel = eval(raw_input('Pick a channel!'))
band = eval(raw_input('Pick a band!'))

zulu.openConnection()

link_status = -1

while link_status < 1:
    link_status = zulu.linkUser()
    print "Link status: %d" % (link_status)

sensorArray = []

while not sensorArray :
    sensorArray = zulu.collectData(channel)
print "elements in sensorArray: %d" % (len(sensorArray))
print str(sensorArray[-10:]).strip('[]')
print "%.6f" % (zulu.channelBand(channel, band))

while 1:
    value = zulu.channelBand(channel, band)
    print "%.6f" % (value)
    print "grumpy man: %d" % ( zulu.moveTheCar(channel, band) )
    time.sleep(0.1)
    
