# import Enum for enumerating commands
from enum import Enum
from typing import Any, Optional, Union

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
    REQUEST     = 6
    ACK         = 7
    PING        = 8
    PONG        = 9
    OTHER       = 10

# ------------------------------------------------------------------------------
# Message Class
#-------------------------------------------------------------------------------

# this class holds information and data about a message
class Message(object):
    """Basic message object class for holding message data to be transmitted"""

    # construct message to be transmitted
    def __init__(self,command: Command = Command.OTHER, data: Optional[dict] = None):
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
    def command(self) -> Command:
        return self._command

    # return the data in the body of this message
    @property
    def data(self) -> Optional[dict]:
        return self._data

    # return the priority of this message
    @property
    def priority(self) -> int:
        return self._command.value

    #---------------------------------------------------------------------------
    # Setters
    #---------------------------------------------------------------------------

    @command.setter
    def command(self,inp: Command):
        self._command = inp

    @data.setter
    def data(self,inp):
        self._data = inp

    #---------------------------------------------------------------------------
    # Serialization
    #---------------------------------------------------------------------------

    # deserialize message into this object
    @classmethod
    def deserialize(cls, data):
        # get command type
        command = Command(int(data[0]))

        # get data
        data = data[1::]

        return Message(command, data)

    # serialize communication for communication
    def serialize(self):
        # | Command | Data of unfixed size |
        #     |             |
        #     v             v
        #     0     +      321    = 0321 <- data to be transmitted
        #

        # hybrid of fixed and dynamic data
        return str(self._command)+str(self._data)
