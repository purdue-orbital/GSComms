# import Enum for enumerating commands
from enum import Enum

# ------------------------------------------------------------------------------
# Command Enums and Quick Conversions
#-------------------------------------------------------------------------------

# Values with the lowest number will have the highest priority
# Enumerated values of launch commands by priority order
class Command(Enum):
    ABORT       = 0
    CUT         = 1
    LAUNCH      = 2
    LOCATION    = 3
    PRESSURE    = 4
    TEMPERATURE = 5
    OTHER       = 6

# ------------------------------------------------------------------------------
# Message Class
#-------------------------------------------------------------------------------

# this class holds information and data about a message
class Message(object):
    """Basic message object class for holding message data to be transmitted"""

    # construct message to be transmitted
    def __init__(self,command = "OTHER",data = ""):
        super(Message, self).__init__()
        # set the command
        self._command = command

        # set the data of this message (if any)
        self._data = data

    #---------------------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------------------

    # return command set in this message
    @property
    def command(self):
        return self._command

    # return the data in the body of this message
    @property
    def data(self):
        return self._data

    # return the priority of this message
    @property
    def priority(self):
        return Command[self._command].value

    #---------------------------------------------------------------------------
    # Setters
    #---------------------------------------------------------------------------

    @command.setter
    def command(self,inp):
        self._command = inp

    @data.setter
    def data(self,inp):
        self._data = inp

    #---------------------------------------------------------------------------
    # Serialization
    #---------------------------------------------------------------------------

    # deserialize message into this object
    def deserialize(self,data):
        # get command type
        self._command = Command(int(data[0])).name

        # get data
        self._data = data[1::]

    # serialize communication for communication
    def serialize(self):
        # | Command | Data of unfixed size |
        #     |             |
        #     v             v
        #     0     +      321    = 0321 <- data to be transmitted
        #

        # hybrid of fixed and dynamic data
        return str(Command[self._command].value)+str(self._data)
