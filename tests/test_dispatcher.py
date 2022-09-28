from time import sleep
from gscomms.common.dispatcher import Dispatcher
from gscomms.common.message import Command

def test_dispatcher_threads():
    dispatcher = Dispatcher()
    dispatcher.start()
    sleep(0.1)
    assert dispatcher.is_running()
    dispatcher.stop()
    assert not dispatcher.is_running()

class PhonySubscriber:
    received = 0

    def rx(self, msg):
        self.received += 1

class PhonyPollableAlways:
    emitted = 0

    def rx(self) -> None:
        self.emitted += 1
        return Command.OTHER

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

    # May not be exact since threads will have been stopped at unknown time, so use margin of error
    assert abs(sub.received - always.emitted) <= 2

    # Empty subscriber shouldn't have received anything
    assert empty_sub.received == 0