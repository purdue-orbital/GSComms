#
# This file will hold instructions and data about proccesing inbound and outbound messages to and from the radio
#

# import heap queue for ease of handling in and bout bound communication
from heap import *

# import messages
from common.message import *

# import seral manager
import serial

# ------------------------------------------------------------------------------
# Message Proccesor Class
#-------------------------------------------------------------------------------

# this class with handle proccessing messges
class mp(object):
    """Message Proccesor (mp) will handle proccesing of messages inbound and outbound"""

    def __init__(self,DEBUG = False):
        super(mp, self).__init__()

        # make the outbound queue
        self.Outbound = FibonacciHeap()

        # make the inbound queue
        self.Inbound = FibonacciHeap()

        #set debug value
        self.DEBUG = DEBUG

    def start(self):
        self.Serial = serial.serial(self.Inbound,self.Outbound,self.DEBUG)
    # takes in a message and add the message to queue
    def transmit(self,inp):
        self.Outbound.insert(inp.get_priority(),inp.serialize())

    # read the next message in queue and returns a message object
    def fetch(self):
        # get the command with the highest priority
        data = self.Inbound.extract_min()

        if data == None:
            return None

        data = data.value

        # set and return a new message object
        m = Message()
        m.deserialize(data)
        return data
