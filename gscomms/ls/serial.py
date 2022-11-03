#
#   This holds data about serial connecto and from the radio
#

# Soapy is the program we use for serial communication to and from the radio
import SoapySDR
from SoapySDR import *
from .heap import *

# import message class
from .message import *

# import time for sleep
from time import sleep

# import threading to run this on it's own thread
import threading

# Global static varables for controlling the radio
RX_CHANNEL = 1
RX_FREQENCY = 233

TX_CHANNEL = 0
TX_FREQENCY = 233


class serial(object):
    """serial is a wrapper for SoapySDR and makes it easy for sending of serialized data to and from the radio"""

    def __init__(self,inbound,outbound,DEBUG = False):
        super(serial, self).__init__()

        # save state of debug
        self.DEBUG = DEBUG

        # store inbound heap
        self.Inbound = inbound

        #   store out bound heap
        self.Outbound = outbound

        #if in debug mode, create files for debug transmissions
        if DEBUG:
            file = open("../"+str(RX_CHANNEL)+str(RX_FREQENCY)+".txt", "w+")
            file.close()

            file = open("../"+str(TX_CHANNEL)+str(TX_FREQENCY)+".txt", "w+")
            file.close()

        # start thread
        threading.Thread(target=self.start).start()



    # this function handles the continous thread of data coming in and out
    def start(self):
        while True:
            # run at 24 updates a second
            sleep(0.041666667)

            # get next input
            inp = self.collect()

            if inp != "" and inp != None:
                # read message and put in priority
                tem = message()
                tem.deserialize(inp)

                # put message into queue
                self.Inbound.insert(tem.get_priority(),inp)

            out = self.Outbound.extract_min()

            if out != None:
                # transmit message from queue
                self.transmit(str(out.value))


    # send transmission on set channel and freqency
    def transmit(self,data):
        # if on debug, make a file imitating the radio
        if(self.DEBUG):
            file = open("../"+str(TX_CHANNEL)+str(TX_FREQENCY)+".txt", "a+")
            file.write(data)
            file.close()
            return
            # End of debug


    # collect transmission on set channel and freqency
    def collect(self):
        out = ""
        # if on debug, make a file imitating the radio
        if(self.DEBUG):
            file = open("../"+str(RX_CHANNEL)+str(RX_FREQENCY)+".txt", "r+")
            out = file.read()
            file.close()

            if out != "":
                file = open("../"+str(RX_CHANNEL)+str(RX_FREQENCY)+".txt", "w+")
                file.write("")
                file.close()
            return out
            # End of # DEBUG:
