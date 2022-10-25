#
# Modulation.py
#
# Author: Nicholas Ball
#
# This file will handle mod and demod of input data to and from the radio
# We are currently using BPSK but QPSK and higher would be possible
#

# Numpy is used by soapysdr so we have to use it here
import numpy as np
import math
np.set_printoptions(threshold=np.inf)


#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------
Phase_Shifts    = 2          # number of possible phase shifts to modulate to (IE: 2 == BPSK and 4 == QPSK)
Sample_Rate     = int(500e3) # rate that modulation works (EX: 500e3 == 500,000 hz or 500 Khz)



# Debug of points to graph
debug_arr = []



#normalize the samples
def normalize(samps):
    samps = samps - np.mean(samps) #remove dc
    samps = np.absolute(samps) #magnitude
    samps = samps / max(samps) #norm ampl to peak
    return samps

#-------------------------------------------------------------------------------
# Modulation class
#-------------------------------------------------------------------------------
class Modulation(object):
    """
        Modulation is important as it takes data points from waves and converts
        them to binary data so the computer can understand them
    """

    # Constructor takes in the carrier signal in hz to make points to
    def __init__(self, carrier_signal_hz,radio_sample_rate,sample_size):
        super(Modulation, self).__init__()

        # Get global values
        global Binary_Options,Sample_Rate

        # Set signal freqency
        self.Carrier_Signal_Hz = carrier_signal_hz

        # Set Binary option from global value
        self.Phase_Shifts = Phase_Shifts

        # Set sample rate of the modulation from global value
        self.Sample_Rate = Sample_Rate

        # Set the number of data points per an offset
        self.Num_Points = radio_sample_rate / Sample_Rate

        # Set the rate at which the radio samples data
        self.Radio_Sample_Rate = radio_sample_rate

        # Set sample size
        self.Sample_Size = sample_size

    # form a wave set with given bit
    def form_wave(self,bit,phi=0.285):
        # make time
        time = np.arange(self.Num_Points) / self.Radio_Sample_Rate

        # Make wave
        # I found this helpful https://en.wikipedia.org/wiki/Phase-shift_keying
        wave = np.cos(((2 * np.pi * self.Carrier_Signal_Hz * time) + (np.pi*(1 - bit)))).astype(np.complex64)

        return (wave * 100)

    # preform the inverse of formming a wave
    def inverse_wave(self,wave,phi=0.285):

        list = []

        time = np.arange(self.Num_Points) / self.Radio_Sample_Rate

        # preform wave inverse
        inverse = -(((np.arccos(wave / 100) - (2 * np.pi * self.Carrier_Signal_Hz * time)) / np.pi) - 1)

        # mod inverse value
        inverse = np.round(np.fmod(inverse.real,2))
        #print(inverse)

        # return if an offset is not detected
        if inverse[0] == 0:
            return "0"
        else:
            return "1"


    # this will take a
    def encode(self,bin):
        out = np.array([0]*0, np.complex64)
        for x in range(len(bin)):
            out = np.concatenate((out,self.form_wave(int(bin[x]))))
        return out

    def decode(self,data):
        bin = ""
        for x in range(int(len(data) / self.Num_Points)):
            bin += self.inverse_wave(data[int(self.Num_Points*x):int(self.Num_Points*x+self.Num_Points)])
        return bin



    def get_debug(self):
        global debug_arr
        return  debug_arr
