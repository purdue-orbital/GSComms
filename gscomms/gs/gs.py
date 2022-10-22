from typing import Optional, Tuple
from common.dispatcher import Dispatcher
from common.message import Command, Message


class GroundStation:
    def __init__(self) -> None:
        self._temperature = None
        self._location = None
        self._pressure = None

        Dispatcher().subscribe(self._on_message, {Command.TEMPERATURE, Command.LOCATION, Command.PRESSURE, Command.OTHER})

    def die(self):
        Dispatcher().unsubscribe(self._on_message, {Command.TEMPERATURE, Command.LOCATION, Command.PRESSURE, Command.OTHER})

    def _on_message(self, msg: Message):
        if msg.command == Command.TEMPERATURE:
            if data := msg.data:
                self._temperature = data['val']
        elif msg.command == Command.PRESSURE:
            if data := msg.data:
                self._pressure = data['val']
        elif msg.command == Command.LOCATION:
            if data := msg.data:
                self._location = (data['loc'], data['acc'])
        else:
            print(f'Received OTHER command with data: {msg.data}')

    def request_temperature(self):
        Dispatcher().push(Message(Command.REQUEST, {'cmd': Command.TEMPERATURE}))

    def request_location(self):
        Dispatcher().push(Message(Command.REQUEST, {'cmd': Command.LOCATION}))

    def request_pressure(self):
        Dispatcher().push(Message(Command.REQUEST, {'cmd': Command.PRESSURE}))

    @property
    def temperature(self) -> Optional[int]:
        return self._temperature

    @property
    def location(self) -> Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
        """
            Returns triplet of coordinates and acceleration
        """
        return self._location

    @property
    def pressure(self) -> Optional[int]:
        return self._pressure

    def launch(self):
        Dispatcher().push(Message(Command.LAUNCH))

    def cut(self):
        Dispatcher().push(Message(Command.CUT))

    def abort(self):
        Dispatcher().push(Message(Command.ABORT))
