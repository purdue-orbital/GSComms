from __future__ import annotations
from dataclasses import dataclass, field
import threading
from .message import Message, Command
from typing import Optional, Set, Union, Callable
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



_subscribed_stations: dict[Callable, Set[Command]] = {}
_subscribed_radios: dict[object, list[_QueueItem]] = {}

def subscribe_station(delegate: Callable, commands: Union[set, Command]):
    """
    Subscribes a delegate function to receive commands of the type `commands`
    """

    # If commands aren't already a set, make them one
    if not isinstance(commands, set):
        commands = {commands}

    # If delegate is already registered, add commands; otherwise, set as new
    if delegate in _subscribed_stations:
            _subscribed_stations[delegate].update(commands)
    else:
        _subscribed_stations[delegate] = commands

def unsubscribe_station(delegate: Callable, commands: Union[set, Command]):
    """
    Unsubscribes the given delegate function from the commands of the type `commands`
    """

    # If commands aren't already a set, make them one
    if not isinstance(commands, set):
        commands = {commands}

    _subscribed_stations[delegate].difference_update(commands)

    # Remove the delegate from the subscriptions if it's not subscribed to anything
    if len(_subscribed_stations[delegate]) == 0:
        _subscribed_stations.pop(delegate)

# Subscribes a radio which calls a function to give the radio a way to pop its queue
def subscribe_radio(delegate):
    _subscribed_radios[delegate] = []

    def pop() -> Optional[Message]:
        if len(_subscribed_radios[delegate]) == 0:
            return None
        val = heappop(_subscribed_radios[delegate]).msg
        return val

    delegate.on_subscribed(pop)

def unsubscribe_radio(delegate):
    _subscribed_radios.pop(delegate)

def push_radios(message: Message):
    """
    Pushes a message to all radios
    """
    for (_, queue) in _subscribed_radios.items():
        heappush(queue, _QueueItem(message))

def push_stations(message: Message):
    for (delegate, _) in filter(lambda kv_pair: message.command in kv_pair[1], _subscribed_stations.items()):
        delegate(message)


PING_TIME_MS = 30_000


# Built-in class for controlling ping-pong behavior
# Pass the entire object in to the subscribe function
# stop must be called before program ends to stop timer
class AckPing:
    def __init__(self, send_pings: bool) -> None:
        self.timer = threading.Timer(PING_TIME_MS / 1000, lambda: push_radios(Message(Command.PING))) if send_pings else None
        if timer := self.timer:
            timer.start()

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