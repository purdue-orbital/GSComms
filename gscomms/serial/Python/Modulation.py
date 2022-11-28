#
# File: Modulation.py
#
# Author(s): Nicholas Ball
#
# Description: This will modulate a given number into a wave to then be handled
#
import numpy as np
from math import *

import warnings

SampleRate = 32e3
ModRatio = 1

# Radio points and convert to binary
def Demod(array):

    # Calculate amplitude
    amplitude = ((array.real ** 2) + (array.imag ** 2)) ** 0.5

    print(amplitude)

    # remove noise
    array = array[amplitude > 0.08]
    '''
    amplitude = amplitude[amplitude > 0.1]
    print(amplitude)
    data = ''
    np.set_printoptions(threshold=np.inf)
    for x in amplitude:
        if x > 0.4:
            data += '1'
        else:
            data += '0'

    '''
    '''
    Ii = (array.real)
    Qi = (array.imag)
    s = np.arctan(Qi / Ii)
    s = np.diff(s)
    print(s)

    one = False

    data = ''
    #print(array.real)

    # convert positive nums to 1 and rest to 0
    for x in range(len(s)):
        if s[x] < 0.5:
            one = not(one)
        if one:
            data += '1'
        else:
            data += '0'
    #'''
    '''
    #FSK v2
    one = False

    data = ''

    I = np.diff(array.real)**2
    Q = np.diff(array.imag)**2
    dis = (I+Q)**0.5
    dis = np.diff(dis)
    #r = np.arctan(np.diff(array.imag) / np.diff(array.real))
    print(dis)
    f = dis

    for x in range(f.size):
        if f[x] < 0.01:
            one = not(one)

        if one:
            data += '1'
        else:
            data += '0'
    '''
    # Pulser
    data = ''

    Is = array.real
    Qs = array.imag[1:]
    Qs = np.append(Qs,[0])

    diff = Is = Qs

    flip = False

    for x in diff:
        if abs(x) > 0.5:
            flip = not (flip)
        print(x)

        if(flip):
            data += '1'
        else:
            data += '0'



    return data

# Modulate data with carrier frequency
def Mod(array,carrier_frequency):

    # IQ Radio formula
    # A⋅(cos(ϕ) + i⋅sin(ϕ)) = A⋅eiϕ = I + Qi <-- This is what soapysdr reads to transmit

    # Phi formula for radio
    # ϕ = 2 * PI * frequency * time

    # Good explenation here: https://www.pe0sat.vgnet.nl/sdr/iq-data-explained/
    np.set_printoptions(threshold=np.inf)
    array = np.repeat(array,ModRatio)

    # create time array
    time = np.arange(array.size) / SampleRate

    # Calculate phi (the angle in radians) for calculation (AKA phase angle)
    phi = 2 * np.pi * carrier_frequency * time


    # BPSK works by offsetting the time in the frequency
    #phi = phi + (np.pi * (1 - array))

    # Calculate phi (the angle in radians) for calculation (AKA phase angle)
    #phi = 2 * np.pi * (carrier_frequency + carrier_frequency * -array) * time # <-- Freqency changes in FSK

    #array[array == 0] = 0.01
    #array[array == 1] = 1

    # Calculate IQ values
    IQ = np.cos(phi) + 1j * np.sin(phi)

    return IQ
