from dataclasses import dataclass, field
import threading
from typing_extensions import Self
from common.message import Command, Message
from typing import Any, Union
from heapq import heappop, heappush

@dataclass(order=True)
class _QueueItem:
    # Declare here to add field attribute
    msg: Message=field(compare=False)

    def __init__(self, msg: Message):
        """
        Initialize queue item
        """

        self.msg = msg

    @property
    def priority(self) -> int:
        """
        Gets priority for queue
        """

        return self.msg.priority


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

        self._queue_lock = threading.Lock()
        self._queue_out = []
        self._queue_in = []
        
        self._set_lock = threading.Lock()
        self._subscribed_delegates = set()
        self._watched_watchables = set()

        self._run_threads = True

        self._watch_thread_hnd = threading.Thread(target=self._watch_thread)
        self._sub_thread_hnd = threading.Thread(target=self._sub_thread)

    # Manages the watcher thread
    def _watch_thread(self):
        pass

    # Manages the subscriber thread
    def _sub_thread(self):
        pass

    def subscribe(self, delegate: function, commands: Union[set, Command]):
        """
        Subscribes a delegate function to receive commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        # If delegate is already registered, add commands; otherwise, set as new
        if delegate in self._subscribed_delegates:
            self._subscribed_delegates[delegate].update(commands)
        else:
            self._subscribed_delegates[delegate] = commands

    def unsubscribe(self, delegate: function, commands: Union[set, Command]):
        """
        Unsubscribes the given delegate function from the commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        self._subscribed_delegates[delegate].remove(commands)

        # Remove the delegate from the subscriptions if it's not subscribed to anything
        if len(self._subscribed_delegates[delegate]) == 0:
            del self._subscribed_delegates[delegate]

    def push(self, message: Message):
        """
        Pushes a message to all watched watchables
        """

        heappush(self._queue_out, _QueueItem(message))

    def watch(self, pollable):
        """
        Registers a pollable item to be polled for messages
        """

        self._watched_watchables.add(pollable)

    def unwatch(self, pollable):
        """
        Removes a pollable item from the watch list
        """

        self._watched_watchables.remove(pollable)

    

    