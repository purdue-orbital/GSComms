from random import choice
from time import sleep
from gscomms.common.dispatcher import AckPing, Dispatcher
from gscomms.common.message import Command, Message

def test_dispatcher_threads():
    dispatcher = Dispatcher()
    dispatcher.start()
    sleep(0.1)
    assert dispatcher.is_running()
    dispatcher.stop()
    assert not dispatcher.is_running()

class PhonySubscriber:
    received = 0

    def rx(self, _):
        self.received += 1

class PhonyPollableAlways:
    emitted = 0

    def rx(self) -> None:
        self.emitted += 1
        return Message(Command.OTHER)

class PhonyPollableNever:
    def rx(self) -> None:
        return None

def test_dispatcher_subscriptions():
    # Tests regular subscriptions
    sub = PhonySubscriber()

    # This subscriber shouldn't receive any events since it will be subscribed to Command.ABORT
    empty_sub = PhonySubscriber()

    # Always produces Command.OTHER
    always = PhonyPollableAlways()

    # Here to make sure Dispatcher can handle None returns
    never = PhonyPollableNever()

    dispatcher = Dispatcher()
    dispatcher.start()
    dispatcher.subscribe(sub.rx, Command.OTHER)
    dispatcher.subscribe(empty_sub.rx, Command.ABORT)
    dispatcher.watch(always)
    dispatcher.watch(never)

    sleep(0.5)

    dispatcher.unsubscribe(sub.rx, Command.OTHER)
    dispatcher.unsubscribe(empty_sub.rx, Command.ABORT)
    dispatcher.unwatch(always)
    dispatcher.unwatch(never)
    dispatcher.stop()

    # Make sure everything is empty
    assert len(dispatcher._subscribed_delegates) == 0
    assert len(dispatcher._watched_watchables) == 0

    # May not be exact since threads will have been stopped at unknown time, so use simple comparison
    assert 0 < sub.received <= always.emitted

    # Empty subscriber shouldn't have received anything
    assert empty_sub.received == 0

class PhonyPollableAck:
    normal_emitted = 0
    ping_emitted = 0
    acks = 0
    pongs = 0
    
    def rx(self):
        res = choice([Command.PING, Command.ABORT])
        if res == Command.PING:
            self.ping_emitted += 1
        else:
            self.normal_emitted += 1

        return Message(res)

    def tx(self, msg: Message):
        if msg.command == Command.PONG:
            self.pongs += 1
        elif msg.command == Command.ACK:
            self.acks += 1

def test_dispatcher_ack_ping():
    poll_ack = PhonyPollableAck()

    # The PhonyPollableAck acts as a PING source, so only send PONGs
    ack = AckPing(send_pings=False)

    dispatcher = Dispatcher()
    dispatcher.start()
    dispatcher.subscribe(ack.rx, ack.command_set())
    dispatcher.watch(poll_ack)

    sleep(0.1)

    ack.stop()
    dispatcher.unwatch(poll_ack)
    dispatcher.unsubscribe(ack.rx, ack.command_set())
    dispatcher.stop()

    assert 0 < poll_ack.pongs <= poll_ack.ping_emitted
    assert 0 < poll_ack.acks <= poll_ack.normal_emitted
