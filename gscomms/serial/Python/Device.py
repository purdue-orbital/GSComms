#
# File: Device.py
#
# Author(s): Nicholas Ball
#
# Description: This will purely interface with the radio connected to the device
#

from SoapySDR import *
import SoapySDR
import numpy as np
import time


# Global values used for starting the radio`
Frequency  = int(915e6)
Channel    = 0
Gain       = 21
SampleRate = int(32e3)


class Device(object):
    """This will purely interface with the radio connected to the device"""

    # Constructor
    def __init__(self):
        super(Device, self).__init__()

        # Set radio details
        sdr = SoapySDR.Device(dict(driver="hackrf"))
        #sdr = SoapySDR.Device(dict(driver="lime"))

        # RX
        sdr.setSampleRate(SOAPY_SDR_RX, Channel, SampleRate)
        sdr.setGain(SOAPY_SDR_RX,Channel, Gain)
        sdr.setFrequency(SOAPY_SDR_RX, Channel, Frequency)
        g1 = sdr.listGains(SOAPY_SDR_TX,0)[0]
        g2 = sdr.listGains(SOAPY_SDR_TX,0)[-1]
        sdr.setGain(SOAPY_SDR_RX,Channel,g1,Gain * 2)
        sdr.setGain(SOAPY_SDR_RX,Channel,g2,Gain * 2)
        #sdr.setBandwidth(SOAPY_SDR_RX, Channel, 1.4e6)
        self.RX_Stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [Channel])

        #TX
        sdr.setSampleRate(SOAPY_SDR_TX, Channel, SampleRate)
        sdr.setGain(SOAPY_SDR_TX,Channel, Gain)
        sdr.setFrequency(SOAPY_SDR_TX, Channel, Frequency)
        g1 = sdr.listGains(SOAPY_SDR_TX,0)[0]
        g2 = sdr.listGains(SOAPY_SDR_TX,0)[-1]
        sdr.setGain(SOAPY_SDR_TX,Channel,g1,Gain * 2)
        sdr.setGain(SOAPY_SDR_TX,Channel,g2,Gain * 2)
        #sdr.setBandwidth(SOAPY_SDR_TX, Channel, 5e6)
        self.TX_Stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32, [Channel])



        # Save radio
        self.SDR = sdr



        #time.sleep(10)

    # Handle transmission of a given numpy array and set a delay in milliseconds
    def TX(self,data, delay = 0):
            # Start stream
            self.SDR.activateStream(self.TX_Stream)

            tx_time_0 = int(self.SDR.getHardwareTime() + 0.1e9) #100ms
            tx_flags = SOAPY_SDR_HAS_TIME | SOAPY_SDR_END_BURST

            # Transmit
            rc = self.SDR.writeStream(self.TX_Stream, [data], data.size, 0,0)

            # Check for any errors
            if rc.ret != data.size:
                print('TX Error {}: {}'.format(rc.ret, rc.ret))

            # Stop the stream
            self.SDR.deactivateStream(self.TX_Stream)


    # Record data for some given amount of time and return numpy array
    def RX(self,seconds = 3):
        # start stream
        N = int(seconds * SampleRate)
        buff = np.empty(N, np.complex64)
        self.SDR.activateStream(self.RX_Stream)


        sr = self.SDR.readStream(self.RX_Stream, [buff], N, timeoutUs=int(seconds*2000000000000000))

        # Check for errors
        rc = sr.ret
        assert rc == N, 'Error Reading Samples from Device (error code = %d)!' % rc

        # Close stream
        #self.SDR.closeStream(self.RX_Stream)

        return buff
