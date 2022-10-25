#
# Device.py
#
# Author: Nicholas Ball
#
# This file will handle communication to and from the radio
#
import SoapySDR
from SoapySDR import *
import threading
import numpy as np
import time

# this is for stopping and starting read proccessign
mux = False

class Device(object):
    """Handle communication to and from radio"""

    def __init__(self, rx_freqency,tx_freqency,rx_gain,tx_gain,rx_channel,tx_channel,sample_rate,sample_size):
        super(Device, self).__init__()

        # Get radio
        self.Radio = SoapySDR.Device(dict(driver="hackrf"))

        #-----------------------------------------------------------------------
        # Set freqencies
        #-----------------------------------------------------------------------
        self.RX_Freqency = rx_freqency
        self.TX_Freqency = tx_freqency

        self.Radio.setFrequency(SOAPY_SDR_RX, rx_channel, rx_freqency)
        self.Radio.setFrequency(SOAPY_SDR_TX, tx_channel, tx_freqency)

        #-----------------------------------------------------------------------
        # Set gain
        #-----------------------------------------------------------------------
        self.RX_Gain = rx_gain
        self.TX_Gain = tx_gain

        self.Radio.setGain(SOAPY_SDR_RX, rx_channel, rx_gain)
        self.Radio.setGain(SOAPY_SDR_TX, tx_channel, tx_gain)

        #-----------------------------------------------------------------------
        # Set freqencies
        #-----------------------------------------------------------------------
        self.RX_Channel = rx_channel
        self.TX_Channel = tx_channel

        #-----------------------------------------------------------------------
        # Data Streams
        #-----------------------------------------------------------------------
        self.RX = None
        self.TX = None

        self.RX_Array = np.array([0]*0, np.complex64)

        #-----------------------------------------------------------------------
        # Miscellaneous
        #-----------------------------------------------------------------------
        self.Sample_Rate = sample_rate
        self.Sample_Size = sample_size

        self.Radio.setSampleRate(SOAPY_SDR_RX, rx_channel, sample_rate)
        self.Radio.setSampleRate(SOAPY_SDR_TX, tx_channel, sample_rate)

        # Set bandwidth of 5 khz
        self.Radio.setBandwidth(SOAPY_SDR_RX, rx_channel, 30e6)
        self.Radio.setBandwidth(SOAPY_SDR_TX, tx_channel, 30e6)

    # Get RX array
    def fetch(self):
        # hold data
        hold = self.RX_Array

        # reset array
        self.RX_Array = np.array([0]*0, np.complex64)

        # return data held on to
        return hold

    # send data to radio for it to transmit
    def write(self,data):
        global mux
        # Hold read procces
        mux = True;

        # write
        status = self.Radio.writeStream(self.TX, [data], len(data), SOAPY_SDR_HAS_TIME | SOAPY_SDR_END_BURST,int(self.Radio.getHardwareTime() + 0.1e9),timeoutUs=int(5e5))

        # Resume read method
        mux = False

    # This function will read from the radio and add what it gets to the array
    def __read_loop(self):
        global mux
        while True:
            # if mux is true, wait here
            while mux:
                pass
            # Make buffer
            buff = np.array([0]*self.Sample_Size, np.complex64)

            # Read from radio
            status = self.Radio.readStream(self.RX, [buff], len(buff),timeoutUs=int(5e5))

            # Ensure there is data and then concatenate buffers
            if status.ret > 0:
                self.RX_Array = np.concatenate((self.RX_Array, buff[:status.ret]))

    # Stop ongoing streams
    def stop(self):
        self.Radio.deactivateStream(self.TX)
        self.Radio.deactivateStream(self.RX)
        self.Radio.closeStream(self.RX)
        self.Radio.closeStream(self.TX)


    # Start streams and spawn read thread
    def start(self):
        # setup streams
        self.RX = self.Radio.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [self.RX_Channel])
        self.TX = self.Radio.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32, [self.TX_Channel])

        # Activate read stream
        #self.Radio.activateStream(self.RX)
        self.Radio.activateStream(self.TX)

        # let things "settle" (FPGA is a thing)
        time.sleep(1)

        # Start read loop on new thread
        #threading.Thread(target=self.__read_loop).start()
