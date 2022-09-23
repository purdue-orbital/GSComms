#
#   Description: This file is the class wrapper/front end class for transmitting
#   data to and from the orbital radio
#

import serial
import mp
from enum import Enum
import time
import threading
import common.message as message
from logging import Log

class Event(Enum):
    LOCATION    = 0
    PRESSURE    = 1
    TEMPERATURE = 2
    UPDATE      = 3 # Event raises when at the end of the pipeline (24 times a second)
    FALL        = 4 # Commands that fall through all set subscriptions

# this function is blank and used as defualt function for required subsricbed events
def blank():
    return

class gs(object):
    """coms class file for communicate to and from the launch station"""

    # constructor for orbital communications
    def __init__(self,DEBUG = False):
        super(gs, self).__init__()

        # set defualt gps location (Purdue Bell Tower)
        self.Location = "40.4273N, 86.9141W"

        # set defualt pressure reading
        self.Pressure = "1"

        # set the defualt internal temperature reading
        self.Temperature = "69"

        # set debug value
        self.Debug = DEBUG

        # set proccesor
        self.Proccesor = mp.mp(DEBUG)

        # subsricbed events
        self.Subscriptions = {"UPDATE": blank,"FALL": blank}

# ------------------------------------------------------------------------------
# Getters
# ------------------------------------------------------------------------------

    # returns location as a String
    def get_location(self) -> str:
        """
             Get current location value

             Return:
                (String): Current Location Value
        """
        return self.Location

    # returns pressure as a String
    def get_pressure(self) -> str:
        """
             Get current pressure value

             Return:
                (String): Current Pressure Value
        """
        return self.Pressure

    # returns location as a String
    def get_temperature(self) -> str:
        """
             Get current temperature value

             Parameters:
                (String): Current temperature Value
        """
        return self.Temperature

# ------------------------------------------------------------------------------
# Transmission Methods
#-------------------------------------------------------------------------------
    # sends abort message
    def send_abort(self):
        """
             Sets a location value

             Parameters:
                inp (String): New Location Value
        """
        Log("[*] Sending abort...")

        # build message
        mes = mp.Message("ABORT")

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] abort sent!")

    # sends cut message
    def send_cut(self):
        """
             Set the pressure reading

             Parameters:
                inp (String): New Pressure Value
        """
        Log("[*] Sending pressure...")

        # build message
        mes = mp.Message("PRESSURE")

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] Pressure sent!")

    # sends location as a float
    def send_launch(self):
        """
             Set the internal temperature reading

             Parameters:
                inp (String): New temperature Value
        """
        Log("[*] Sending temperature...")

        # build message
        mes = mp.Message("LAUNCH")

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] Temperature sent!")

    # sends custom data
    def send_data(self,com:str,data:str):
        """
            ***Intended for sending data when the actual command is being worked on***
             Set data under the OTHER command header

             Parameters:
                inp (String): Custom data being sent
        """
        Log("[*] Sending command...")

        # build message
        mes = mp.Message("OTHER",data)

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] Command sent!")

# ------------------------------------------------------------------------------
# Pipeline Methods
#-------------------------------------------------------------------------------
    # runs a function upon receiving a message of specified type. (EX: a function subsricbed to the ABORT command will be activated when an abort command is recived)
    def subscribe(self,flag,function):
        self.Subscriptions[flag.name] = function

    # start running the pipeline and begin listening to the radio
    def start(self):
        # start the message proccesor
        self.Proccesor.start()

        # Loop through proccesing and collecting radio transmission 24 times a second
        while True:
            # wait
            time.sleep(0.041666667)

            # get next in queue
            out = self.Proccesor.fetch()

            # as long as the message out is not empty, continue with the pipeline
            if out != None:

                # make serialized data into a message object
                mes = message.Message()
                mes.deserialize(out)

                # handle message if it is setting values
                if mes.get_command() == "LOCATION":
                    self.Location = mes.data
                elif mes.get_command()  == "PRESSURE":
                    self.Pressure = mes.data
                elif mes.get_command() == "TEMPERATURE":
                    self.Temperature = mes.data

                try:
                    # try to run the subsription message
                    self.Subscriptions[mes.get_command()]()
                except Exception as e:
                    # if it fails to run, run fallthrough code
                    Log("[!] Error detected or uncaught command! Running fallthrough...")

                    # run fallthrough code
                    self.Subscriptions["FALL"]()

            # update function
            self.Subscriptions["UPDATE"]()
        # End of start
