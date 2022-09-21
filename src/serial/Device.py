#
# Device.py
#
# Author: Nicholas Ball
#
# This file will handle radio devices connected to this device and selecting them
#

import SoapySDR
from SoapySDR import *
import numpy as np
import numpy
import sys

# These are used for passing to the radio what kind of stream is happening
RX = 0
TX = 1

# Remove annoying soapysdr stuff
def log_handler(log_level, message):
    pass
SoapySDR.registerLogHandler(log_handler)


# class for device information
class Device(object):
    """Device object holds device information and capabilities"""

    def __new__(self):
        # Make device a signle ton
        if not hasattr(self, 'instance'):
            # Set instance
            self.instance = super(Device, self).__new__(self)

            # Set radio object
            self.Radio = None

            # Set freqency range
            self.Range = []

            # Set Radio transmissions
            self.Streams = {0:None,1:None}

            # Buffer of data\
            self.Buff = numpy.array([0]*1024, numpy.complex64)
        return self.instance

    # This will start a stream
    def start(self,flag,sample_rate,freqency,channel):
        # call global vars
        global RX,TX

        # create object used for setting up the stream
        f = None

        # set the flag
        if flag == RX:
            f = SOAPY_SDR_RX
        else:
            f = SOAPY_SDR_TX

        # Set sample rate
        self.Radio.setSampleRate(f,0,sample_rate)

        # Set freqency
        self.Radio.setFrequency(f,0,freqency)

        self.Radio.setGainMode(f,0,False)

        # setup stream
        self.Streams[flag] = self.Radio.setupStream(f,SOAPY_SDR_CF32,[channel])

        # start stream
        self.Radio.activateStream(self.Streams[flag])

    # Stop a stream that is currently going
    def stop(self,flag):
        # stop the stream
        self.Radio.deactivateStream(self.Streams[flag])
        self.Radio.closeStream(self.Streams[flag])

    # Collect data from the read stream that started
    def read(self):
        return self.Radio.readStream(self.Streams[RX], [self.Buff], len(self.Buff),timeoutUs=int(5e5))

    # Collect data from the read stream that started
    def write(self,data):
        # write data to stream to be transmited
        self.Radio.readStream(self.Streams[TX], [data], len(data)).ret


    def get(self):
        '''
        Get the lime sdr device plugged into this device

        Return:
            Limesdr Device Object or None
        '''
        try:
            self.Radio = SoapySDR.Device(dict(driver="lime"))
        except Exception as e:
            self.Radio = None
