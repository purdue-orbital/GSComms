from dataclasses import dataclass, field
import threading
from time import sleep
from .message import Message, Command
from typing import Any, Union, Callable
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

        self._queue_lock = threading.Lock()
        self._queue_out = []
        self._queue_in = []
        
        self._set_lock = threading.Lock()
        self._subscribed_delegates = {}
        self._watched_watchables = set()

        self._run_threads = True
        self.start()

    def start(self):
        if self.is_running():
            return

        self._watch_thread_hnd = threading.Thread(target=self._watch_thread)
        self._watch_thread_hnd.start()
        self._sub_thread_hnd = threading.Thread(target=self._sub_thread)
        self._sub_thread_hnd.start()

    def is_running(self) -> bool:
        if not (hasattr(self, '_watch_thread_hnd') and hasattr(self, '_sub_thread_hnd')):
            return False

        return self._watch_thread_hnd.is_alive() or self._sub_thread_hnd.is_alive()

    def stop(self):
        self._run_threads = False
        self._watch_thread_hnd.join()
        self._sub_thread_hnd.join()

    # Manages the watcher thread
    def _watch_thread(self):
        while self._run_threads:
            with self._queue_lock:
                # Check output queue and write if necessary
                message = heappop(self._queue_out).msg if len(self._queue_out) > 0 else None

                with self._set_lock:
                    for watchable in self._watched_watchables:
                        if message is not None:
                            watchable.tx(message)
                        # Check pollables and write to input if necessary
                        if msg := watchable.rx():
                            heappush(self._queue_in, _QueueItem(msg))

            sleep(THREAD_SLEEP_MS / 1000)

    # Manages the subscriber thread
    def _sub_thread(self):
        while self._run_threads:
            with self._queue_lock:
                if len(self._queue_in) == 0:
                    continue

                message = heappop(self._queue_in).msg
                with self._set_lock:
                    for (delegate, _) in filter(lambda kv_pair: message in kv_pair[1], self._subscribed_delegates.items()):
                        delegate(message)
            sleep(THREAD_SLEEP_MS / 1000)

    def subscribe(self, delegate: Callable, commands: Union[set, Command]):
        """
        Subscribes a delegate function to receive commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        # If delegate is already registered, add commands; otherwise, set as new
        with self._set_lock:
            if delegate in self._subscribed_delegates:
                self._subscribed_delegates[delegate].update(commands)
            else:
                self._subscribed_delegates[delegate] = commands

    def unsubscribe(self, delegate: Callable, commands: Union[set, Command]):
        """
        Unsubscribes the given delegate function from the commands of the type `commands`
        """

        # If commands aren't already a set, make them one
        if not isinstance(commands, set):
            commands = {commands}

        with self._set_lock:
            self._subscribed_delegates[delegate].difference_update(commands)

            # Remove the delegate from the subscriptions if it's not subscribed to anything
            if len(self._subscribed_delegates[delegate]) == 0:
                del self._subscribed_delegates[delegate]

    def push(self, message: Message):
        """
        Pushes a message to all watched watchables
        """

        with self._queue_lock:
            heappush(self._queue_out, _QueueItem(message))

    def watch(self, pollable):
        """
        Registers a pollable item to be polled for messages
        """

        with self._set_lock:
            self._watched_watchables.add(pollable)

    def unwatch(self, pollable):
        """
        Removes a pollable item from the watch list
        """

        with self._set_lock:
            self._watched_watchables.remove(pollable)

    

    