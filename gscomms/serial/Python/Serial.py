#
# File: Serial.py
#
# Author(s): Nicholas Ball
#
# Description: This file will be directly interfaced for communication to and
# from the radio
#
import Device
from Modulation import *
from matplotlib import pyplot as plt
import viterbi



Frequency  = int(915e6)
Channel    = 0
Gain       = 64
SampleRate = int(32e3)

counter = 0

class Serial(object):
    """Serial is the interface for sending and listening for radio transmissions"""

    def __init__(self):
        super(Serial, self).__init__()
        self.Device = Device.Device()

    def TX(self,data):
        '''
        Pass a string to be transmitted from the radio
        '''
        # Test data for now
            #   0000001
            #   0011001
        data = '1111111111111111111111111'

        # encode for ECC
        #data = viterbi.Encode(data)

        # Convert to numpy array
        bin = np.array(list(data)).astype(float)

        # Modulate data
        out = Mod(bin,Frequency)

        #print(out)
        #print(Demod(out))

        '''
        s = out
        plt.figure(num=1, figsize=(12.95, 7.8), dpi=150)
        plt.subplot(211)
        t_us = np.arange(s.size) / Frequency / 1e-6
        plt.plot(t_us, s.real, 'k', label='I')
        plt.plot(t_us, s.imag, 'r', label='Q')
        plt.xlim(t_us[0], t_us[-1])
        plt.xlabel('Time (us)')
        plt.ylabel('Normalized Amplitude')
        plt.show()
        #'''

        # Transmit
        self.Device.TX(out)



    def RX(self):
        '''
        This will return all collected data that was transmitted
        '''
        global counter

        data = self.Device.RX()

        #s = data

        '''
        if counter == 10:
            plt.figure(num=1, figsize=(12.95, 7.8), dpi=150)
            plt.subplot(211)
            t_us = np.arange(s.size) / Frequency / 1e-6
            plt.plot(t_us, s.real, 'k', label='I')
            plt.plot(t_us, s.imag, 'r', label='Q')
            plt.xlim(t_us[0], t_us[-1])
            plt.xlabel('Time (us)')
            plt.ylabel('Normalized Amplitude')
            plt.show()
        #'''

        # Demod collected data
        out = Demod(data)

        #print(out)

        # Error correct demoded data
        #out = '000' + out[3:-3]+'000'
        #out = out[7:]
        print(out)

        #if len(out) >= 12:
        #    out = viterbi.Decode(out[:12])
        #    print(out)

        #print("1011110001110001" in out)
        print(out)
        print('1' in out)
        counter += 1
