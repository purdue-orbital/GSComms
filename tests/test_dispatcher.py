from time import sleep
from gscomms.common.dispatcher import Dispatcher
from gscomms.common.message import Command

def test_dispatcher_threads():
    dispatcher = Dispatcher()
    dispatcher.start()
    sleep(0.1)
    dispatcher.stop()
    assert not dispatcher.is_running()

class PhonySubscriber:
    received = 0

    def rx(self, msg):
        self.received += 1

class PhonyPollableAlways:
    def rx(self) -> None:
        return Command.OTHER

class PhonyPollableNever:
    def rx(self) -> None:
        return None

def test_dispatcher_subscriptions():
    sub = PhonySubscriber()
    always = PhonyPollableAlways()
    never = PhonyPollableNever()

    dispatcher = Dispatcher()
    dispatcher.start()
    dispatcher.subscribe(sub.rx, Command.OTHER)
    dispatcher.watch(always)
    dispatcher.watch(never)

    sleep(0.5)

    dispatcher.unsubscribe(sub.rx, Command.OTHER)
    dispatcher.unwatch(always)
    dispatcher.unwatch(never)
    dispatcher.stop()

    assert len(dispatcher._subscribed_delegates) == 0
    assert sub.received > 0