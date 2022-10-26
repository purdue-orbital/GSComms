from typing import Optional, Tuple
from common.dispatcher import subscribe_station, unsubscribe_station, push_radios
from common.message import Command, Message


class GroundStation:
    def __init__(self) -> None:
        self._temperature = None
        self._location = None
        self._pressure = None

        subscribe_station(self._on_message, {Command.TEMPERATURE, Command.LOCATION, Command.PRESSURE, Command.OTHER})

    def die(self):
        unsubscribe_station(self._on_message, {Command.TEMPERATURE, Command.LOCATION, Command.PRESSURE, Command.OTHER})

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
        push_radios(Message(Command.REQUEST, {'cmd': Command.TEMPERATURE}))

    def request_location(self):
        push_radios(Message(Command.REQUEST, {'cmd': Command.LOCATION}))

    def request_pressure(self):
        push_radios(Message(Command.REQUEST, {'cmd': Command.PRESSURE}))

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
        push_radios(Message(Command.LAUNCH))

    def cut(self):
        push_radios(Message(Command.CUT))

    def abort(self):
        push_radios(Message(Command.ABORT))
