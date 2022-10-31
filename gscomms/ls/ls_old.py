from . import serial
from . import mp
from enum import Enum
import time
from .logging import Log

class Event(Enum):
    ABORT       = 0
    CUT         = 1
    LAUNCH      = 2
    UPDATE      = 3 # Event raises when at the end of the pipeline (24 times a second)
    FALL        = 4 # Commands that fall through all set subscriptions

# this function is blank and used as defualt function for required subsricbed events
def blank():
    return

class ls():
    def __init__(self,DEBUG = False):
            super(ls, self).__init__()

            # make a new instance of a messgae proccesor
            self.Proccesor = mp.mp(DEBUG)

            # set if this program is under going debugging
            self.Debug = DEBUG

            # dictionary of subsricbed events
            self.Subscriptions = {"UPDATE": blank,"FALL": blank}

# ------------------------------------------------------------------------------
# Transmission Methods AKA "Senders"
#-------------------------------------------------------------------------------
    # sends location as a String
    def send_location(self,inp:str):
        """
             Sets a location value

             Parameters:
                inp (String): New Location Value
        """
        Log("[*] Sending location...")

        # build message
        mes = mp.message("LOCATION",inp)

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] Location sent!")

    # sends pressure as a float
    def send_pressure(self,inp:float):
        """
             Set the pressure reading

             Parameters:
                inp (String): New Pressure Value
        """
        Log("[*] Sending pressure...")

        # build message
        mes = mp.message("PRESSURE",inp)

        # send message
        self.Proccesor.transmit(mes)

        Log("[!] Pressure sent!")

    # sends location as a float
    def send_temperature(self,inp:float):
        """
             Set the internal temperature reading

             Parameters:
                inp (String): New temperature Value
        """
        Log("[*] Sending temperature...")

        # build message
        mes = mp.message("TEMPERATURE",inp)

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
        mes = mp.message("OTHER",data)

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
        self.Proccesor.start()
        # Loop through proccesing and collecting radio transmission 24 times a second
        while True:
            # wait
            time.sleep(0.041666667)

            # get next in queue
            out = self.Proccesor.fetch()

            # as long as the message out is not empty, continue with the pipeline
            if out != None:
                try:
                    # try to run the subsricbed message
                    self.Subscriptions[out.Command]()
                except Exception as e:
                    Log("[!] Error detected or uncaught command! Running fallthrough...")

                    # try to run fallthrough
                    self.Subscriptions["FALL"]()

            # update function
            self.Subscriptions["UPDATE"]()
        # End of start
