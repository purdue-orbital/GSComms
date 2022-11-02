from gscomms.common.message import Command, Message
import pytest


def test_serialization():
    assert Message(Command.ABORT).serialize() == f'{Command.ABORT.value}'

    assert Message(Command.REQUEST, {'cmd': Command.TEMPERATURE}).serialize() == f'{Command.REQUEST.value}' + "{" + f'"cmd": {Command.TEMPERATURE.value}' + "}"

def test_deserialization():
    msg = Message.deserialize('0')

    assert msg.command == Command.ABORT
    assert msg.data is None

    with pytest.raises(ValueError):
        Message.deserialize('20')