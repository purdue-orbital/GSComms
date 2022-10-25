from dataclasses import dataclass, field
import threading
from time import sleep
from .message import Message, Command
from typing import Any, Optional, Set, Union, Callable
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


# Time for dispatcher threads to sleep (ms)
THREAD_SLEEP_MS = 5


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
        self._subscribed_stations: dict[Callable, Set[Command]] = {}
        self._subscribed_radios: dict[object, list[_QueueItem]] = {}

    def subscribe_station(self, delegate: Callable, commands: Union[set, Command]):
        """
        Subscribes a delegate function to receive commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        # If delegate is already registered, add commands; otherwise, set as new
        if delegate in self._subscribed_stations:
                self._subscribed_stations[delegate].update(commands)
        else:
            self._subscribed_stations[delegate] = commands

    def unsubscribe_station(self, delegate: Callable, commands: Union[set, Command]):
        """
        Unsubscribes the given delegate function from the commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        self._subscribed_stations[delegate].difference_update(commands)

        # Remove the delegate from the subscriptions if it's not subscribed to anything
        if len(self._subscribed_stations[delegate]) == 0:
            self._subscribed_stations.pop(delegate)

    # Subscribes a radio which calls a function to give the radio a way to pop its queue
    def subscribe_radio(self, delegate):
        self._subscribed_radios[delegate] = []

        def pop() -> Optional[Message]:
            if len(self._subscribed_radios[delegate]) == 0:
                return None
            return heappop(self._subscribed_radios[delegate]).msg

        delegate.on_subscribed(pop)

    def unsubscribe_radio(self, delegate):
        self._subscribed_radios.pop(delegate)

    def push_radios(self, message: Message):
        """
        Pushes a message to all radios
        """
        for (_, queue) in self._subscribed_radios.items():
            heappush(queue, _QueueItem(message))

    def push_stations(self, message: Message):
        for (delegate, _) in filter(lambda kv_pair: message.command in kv_pair[1], self._subscribed_stations.items()):
            delegate(message)


PING_TIME_MS = 30_000


# Built-in class for controlling ping-pong behavior
# Pass the entire object in to the subscribe function
# stop must be called before program ends to stop timer
class AckPing:
    def __init__(self, send_pings: bool) -> None:
        self.timer = threading.Timer(PING_TIME_MS / 1000, lambda: Dispatcher().push_radios(Message(Command.PING))) if send_pings else None

    def rx(self, message: Message):
        if message.command == Command.PING:
            return Message(Command.PONG)
        else:
            return Message(Command.ACK, {'cmd': message})

    def stop(self):
        if timer := self.timer:
            timer.cancel()

    @property
    def command_set(self) -> set:
        """
        Commands to be passed as the second argument of the subscribe function
        """

        return {
            Command.ABORT, 
            Command.CUT, 
            Command.LAUNCH, 
            Command.LOCATION, 
            Command.OTHER, 
            Command.PING, 
            Command.PRESSURE, 
            Command.TEMPERATURE
        }