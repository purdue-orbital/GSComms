# import Enum for enumerating commands
from enum import IntEnum
from typing import Any, Optional, Union
from json import dumps, loads

# ------------------------------------------------------------------------------
# Command Enums and Quick Conversions
#-------------------------------------------------------------------------------

# Values with the lowest number will have the highest priority
# Enumerated values of launch commands by priority order
class Command(IntEnum):
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
    def deserialize(cls, data: str):
        # get command type
        arr = data.split('{')

        cmd= arr[0]
        payload = arr[1] if len(arr) > 1 else None

        command = Command(int(cmd))

        return Message(command, loads(payload) if payload is not None else None)

    # serialize communication for communication
    def serialize(self):
        # | Command | Data of unfixed size |
        #     |             |
        #     v             v
        #     0     +      321    = 0321 <- data to be transmitted
        #

        # hybrid of fixed and dynamic data
        return str(self.command.value) + (dumps(self.data) if self.data is not None else '')

    def to_string(self):
        return f'Message: Command: {self.command} Data: {self.data}'
