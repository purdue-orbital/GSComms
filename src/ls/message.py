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
class message(object):
    """Basic message object class for holding message data to be transmitted"""

    # construct message to be transmitted
    def __init__(self,command = "OTHER",data = ""):
        super(message, self).__init__()
        # set the command
        self.Command = command

        # set the data of this message (if any)
        self.Data = data

    #---------------------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------------------

    # return command set in this message
    def get_command(self):
        return self.Command

    # return the data in the body of this message
    def get_data(self):
        return self.Data

    # return the priority of this message
    def get_priority(self):
        return Command[self.Command].value

    #---------------------------------------------------------------------------
    # Setters
    #---------------------------------------------------------------------------

    def set_command(self,inp):
        self.Command = inp

    def set_data(self,inp):
        self.Data = inp

    #---------------------------------------------------------------------------
    # Serialization
    #---------------------------------------------------------------------------

    # deserialize message into this object
    def deserialize(self,data):
        # get command type
        self.Command = Command(int(data[0])).name

        # get data
        self.Data = data[1::]

    # serialize communication for communication
    def serialize(self):
        # | Command | Data of unfixed size |
        #     |             |
        #     v             v
        #     0     +      321    = 0321 <- data to be transmitted
        #

        # hybrid of fixed and dynamic data
        return str(Command[self.Command].value)+str(self.Data)
