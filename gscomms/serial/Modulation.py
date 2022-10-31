#
# File: Modulation.py
#
# Author(s): Nicholas Ball
#
# Description: This will modulate a given number into a wave to then be handled
#
import numpy as np

import warnings

SampleRate = 32e3
ModRatio = 4


# take amplitude and convert to values
def Demod(array):


    # Calculate amplitude
    amplitude = ((array.real ** 2) + (array.imag ** 2)) ** 0.5

    np.set_printoptions(threshold=np.inf)

    # convert amplitudes to binary data
    amplitude[amplitude > 0.5] = 1
    amplitude[amplitude <= 0.5] = 0

    # Average values over time
    tem = np.empty(array.size)
    for x in range(0,array.size - ModRatio):
        tem[x] = np.average(array[x:x+ModRatio-1])

    #print(tem)
    print(amplitude)

    return tem

# Modulate data with carrier frequency
def Mod(array,carrier_frequency):

    # Radio formula
    # A⋅(cos(ϕ) + i⋅sin(ϕ)) = A⋅eiϕ = I + Qi <-- This is what soapysdr reads to transmit

    # Phi formula for radio
    # ϕ = 2 * PI * frequency * time

    # Good explenation here: https://www.pe0sat.vgnet.nl/sdr/iq-data-explained/

    # repeat values
    array = array.repeat(ModRatio)

    # create time array
    time = np.arange(array.size) / SampleRate

    # Calculate phi (the angle in radians) for calculation (AKA phase angle)
    phi = 2 * np.pi * carrier_frequency * time

    # Calculate IQ values
    IQ = array * (np.cos(phi) + 1j * np.sin(phi))

    print(IQ)

    return IQ
