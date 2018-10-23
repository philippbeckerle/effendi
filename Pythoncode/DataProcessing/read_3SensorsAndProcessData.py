#!usr/bin/env python
# many code parts taken from http://electronut.in/plotting-real-time-data-from-arduino-using-python/

# this code reads the serial input of com7, which is always one value that is read out from one force pressure sensor. The data is safed
# into a file and a live plot takes place


import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


strPort = 'com10'
cnt = 0



# plot class
class AnalogPlot:
    def __init__(self, strPort, maxLen):
        '''
        deques are data containers that can be rapidly accessed for reading and writing. Those
        containers will temporarily save the values that are read out from the sensors and will be
        plotted onto the y axis. maxLen is the maximum number of values that are stored in the deques.
        The Baud Rate of Serial has to be the same as the Baud rate of the Arduino.
        '''
        # open serial port
        self.ser = serial.Serial(strPort, 9600)

        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.az = deque([0.0] * maxLen)
        self.maxLen = maxLen

    def addToBuf(self, buf, val):
        '''
        the current read out values are appended to the deques. buf.pop() deletes the oldest value in the
        deques.
        '''
        if len(buf) < self.maxLen:
            buf.append(val)

        else:
            buf.pop()
            buf.appendleft(val) #ax list is updated with the current value from the readout

    def add(self, data):
        '''
        this function calls the addToBuf function that adds the read out values to the buffer.
        '''
        assert (len(data) == 3)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])
        self.addToBuf(self.az, data[2])

    def update(self, frameNum, a0, a1, a2):
        '''
        the update function is continously called by FuncAnimation. The str data from the serial port
        are converted to floats and later written to a txt.file. "frameNum" in the arguments of the function is needed
        that FunkAnimation knows that update function has to be continously called.
        '''
        global cnt
        try:
            line = self.ser.readline()
            #print line
            #y = line.split(";")
            #print(y.decode('utf-8'))

            convertList = (line.split(";"))[0:3]

            try:
                data = [float(val) for val in convertList] # line.split is important if more than 2 values are sent over the serial port by the Arduino
                #print data
                if len(data) == 3:
                    self.add(data)
                    a0.set_data(range(self.maxLen), self.ax)
                    a1.set_data(range(self.maxLen), self.ay)
                    a2.set_data(range(self.maxLen), self.az)

                    string = str(cnt) + "," + str(data) + "\n"

                    f = open("test.txt", "a+")
                    f.write(string)
                    f.close()
                    cnt += 1
            except:
                print 'error in conversion'


        except KeyboardInterrupt:
            print('exiting')

        return a0,

    def close(self):
        ''' close the Serial Ports when program is ended.'''
        # close serial
        self.ser.flush()
        self.ser.close()


def main():
    print('reading from serial port %s...' % strPort)

    # plot parameters
    analogPlot = AnalogPlot(strPort, 100)

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    a2, = ax.plot([], [])
    print "hello"
    anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, a1, a2), interval=20)

    try:
    # show plot
        plt.show()
    except:
        pass


    analogPlot.close()

    # clean up
    print('exiting.')


# call main
if __name__ == '__main__':
    main()
