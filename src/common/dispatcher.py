

from common.message import Command, Message
from typing import Union


class Dispatcher(object):
    def __new__(cls):
        """
        Creates and manages a single instance of the Dispatcher class
        """
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(Dispatcher, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """
        Initializes member variables
        """

        self.__queue_out = []
        self.__queue_in = []

    def subscribe(delegate: function, commands: Union[list, Command]):
        """
        Subscribes a delegate function to receive commands of the type `commands`
        """

        pass

    def unsubscribe(delegate: function, commands: Union[list, Command]):
        """
        Unsubscribes the given delegate function from the commands of the type `commands`
        """

        pass

    def push(message: Message):
        """
        Pushes a message to all watched watchables
        """

        pass

    def watch(pollable):
        """
        Registers a pollable item to be polled for messages
        """

        pass

    def unwatch(pollable):
        """
        Removes a pollable item from the watch list
        """

        pass

    

    