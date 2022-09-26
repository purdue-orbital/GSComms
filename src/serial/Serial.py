#
# Serial.py
#
# Author: Nicholas Ball
#
# This file is used as the interface into handling serial communication to and
# from the radio
#



class Serial(object):
    """docstring for Serial."""

    # Serial is a sigleton (Only has one instance of itself)
    def __new__(self):
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
            self.Buff = numpy.array([0]*100, numpy.complex64)
        return self.instance
