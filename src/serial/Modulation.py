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

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------
Phase_Shifts    = 2          # number of possible phase shifts to modulate to (IE: 2 == BPSK and 4 == QPSK)
Sample_Rate     = int(500e3) # rate that modulation works (EX: 500e3 == 500,000 hz or 500 Khz)

#-------------------------------------------------------------------------------
# Modulation class
#-------------------------------------------------------------------------------
class Modulation(object):
    """
        Modulation is important as it takes data points from waves and converts
        them to binary data so the computer can understand them
    """

    # Constructor takes in the carrier signal in hz to make points to
    def __init__(self, carrier_signal_hz,radio_sample_rate):
        super(Modulation, self).__init__()

        # Get global values
        global Binary_Options,Sample_Rate

        # Set signal freqency
        self.Carrier_Signal_Hz = carrier_signal_hz

        # Set Binary option from global value
        self.Phase_Shifts = Phase_Shifts

        # Set sample rate of the modulation from global value
        self.Sample_Rate = Sample_Rate

        # Set the rate at which the radio samples data
        self.Radio_Sample_Rate = radio_sample_rate

        # Set the margin of error for decodeding
        self.Margin = 5 / (Phase_Shifts / 2)

    # This is used to calculate the points on the signal (Wave shift math)
    # I found this helpful: https://en.wikipedia.org/wiki/Phase-shift_keying
    def calculate(self,bit,time):
        # Amplitude of the signal. PSK doesn't need it to change since it
        # doesn't use  amplitude as a means of communication. However, QAM does
        # so it is here if we want to use it in the future
        a = 10

        # Take half of the number of phase shifts
        half = (self.Phase_Shifts/2)

        # Convert number repesentation of bit(s) to a radian
        #rad = (int(bit, 2) - (1)) * (math.pi / half)
        rad = (int(bit, 2) - (1/half)) * (math.pi / half)
        #rad = (int(bit, 2)*2 - (1)) * (math.pi / 4)

        # Make and return data point
        return a * math.cos(2.0 * math.pi * self.Carrier_Signal_Hz * time + rad)


    # Encode string of binary into wave points
    def encode(self,data,streams = 1):
        # Make the binary into a encodable size by adding zeros at the beginning
        while len(data) % (Phase_Shifts/2) != 0:
            data = "0"+data

        # Break up the binary into phase shiftable points
        data = [data[i:i+int(self.Phase_Shifts/2)] for i in range(0, len(data), int(self.Phase_Shifts/2))]

        # Calculate rate at which to advance time
        rate = 1 / self.Radio_Sample_Rate

        # Calculate the number of data points per a bit so it can be transmited
        num_points =  int(self.Radio_Sample_Rate  / self.Sample_Rate)

        # Time that currently on for calculation
        time = 0.0

        # Array of data points to return
        arr = []

        # Loop through bits to be encoded
        for x in data:

            # Loop through number of samples per a value
            for t in range(num_points):

                # Preform calculation
                arr.append(self.calculate(x,time))

                # Advance time by rate
                time += rate

                # End of loop for making samples

            #  End loop for each set of binary chars

        print(arr)

        # Return array
        return np.array(arr)

    # Reverse calculation and get the bit from a wave point given time and freqency
    def decalculate(self,point,time):
        # preform the inverse wave function on point and time
        inverse = (-2 * math.pi * time * self.Carrier_Signal_Hz) + math.acos((point / 10))

        # get the bit numarical value out of the inverse
        n = ((inverse / (math.pi / (self.Phase_Shifts / 2))) + 1) % self.Phase_Shifts

        # return number in binary format
        return ('{0:0'+str(int(self.Phase_Shifts/2))+'b}').format(round(n))

    # Take a batch of samples and decode it into binary
    def decode(self,data,streams = 1):
            # Calculate rate at which to advance time
            rate = self.Radio_Sample_Rate / self.Sample_Rate

            # get the number of time to advance time
            num_loop = int(data.size / rate)

            # Time that currently on for calculation
            time = 0

            # value to return after decodeing
            toReturn = ""

            for x in range(num_loop):
                # get data point
                value = data[int(x*rate)]

                # preform inverse calculation and return a string
                value = self.decalculate(value,time)

                # Add value to return
                toReturn += value

                # advance time
                time += rate / self.Radio_Sample_Rate

            # Return decoded value
            return toReturn
