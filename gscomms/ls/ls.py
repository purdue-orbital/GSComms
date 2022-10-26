from common.message import Command, Message
from common.dispatcher import Dispatcher


class LaunchStation:
    def __init__(self) -> None:
        self.is_aborted = False
        self.is_cut = False
        self.is_launched = False
        self.current_temperature = None
        self.current_gps = None
        self.current_acceleration = None
        self.current_pressure = None
        self.last_other_data = None

        Dispatcher().subscribe_station(self._on_message, {Command.ABORT, Command.CUT, Command.LAUNCH, Command.REQUEST, Command.OTHER})

    def die(self):
        Dispatcher().unsubscribe_station(self._on_message, {Command.ABORT, Command.CUT, Command.LAUNCH, Command.REQUEST, Command.OTHER})

    def _on_message(self, msg: Message):
        if msg.command == Command.ABORT:
            self.is_aborted = True
        elif msg.command == Command.CUT:
            self.is_cut = True
        elif msg.command == Command.LAUNCH:
            self.is_launched = True
        elif msg.command == Command.REQUEST:
            if data := msg.data:
                command = data['cmd']
                if command == Command.LOCATION:
                    return Message(Command.LOCATION, {'loc': self.current_gps, 'acc': self.current_acceleration})
                elif command == Command.TEMPERATURE:
                    return Message(Command.TEMPERATURE, {'val': self.current_temperature})
                elif command == Command.PRESSURE:
                    return Message(Command.PRESSURE, {'val': self.current_pressure})
        else:
            self.last_other_data = msg.data
