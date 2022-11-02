from random import choice
from time import sleep
from gscomms.common.dispatcher import push_radios, push_stations, subscribe_radio, subscribe_station, unsubscribe_radio, unsubscribe_station, _subscribed_stations, _subscribed_radios
from gscomms.common.message import Command, Message

class PhonySubscriber:
    received = 0

    def rx(self, _):
        self.received += 1

def test_dispatcher_subscriptions():
    # Tests regular subscriptions
    sub = PhonySubscriber()

    # This subscriber shouldn't receive any events since it will be subscribed to Command.ABORT
    empty_sub = PhonySubscriber()

    # This subscriber should receive an event since it's subscribed to Command.OTHER

    subscribe_station(sub.rx, Command.OTHER)
    subscribe_station(empty_sub.rx, Command.ABORT)

    push_stations(Message(Command.OTHER))

    unsubscribe_station(sub.rx, Command.OTHER)
    unsubscribe_station(empty_sub.rx, Command.ABORT)

    # Make sure everything is empty
    assert len(_subscribed_stations) == 0

    # Should have received one message
    assert sub.received == 1

    # Empty subscriber shouldn't have received anything
    assert empty_sub.received == 0

class PhonyRadio:
    def on_subscribed(self, pop):
        self.pop = pop

    def check_pop_queue(self):
        return self.pop() is not None

def test_dispatcher_radios():
    radio = PhonyRadio()

    subscribe_radio(radio)

    push_radios(Message(Command.OTHER))
    push_radios(Message(Command.ABORT))

    # Make sure it received two messages
    assert radio.check_pop_queue()
    assert radio.check_pop_queue()

    unsubscribe_radio(radio)

    # Make sure dispatcher is clean
    assert len(_subscribed_radios) == 0


# class PhonyPollableAck:
#     normal_emitted = 0
#     ping_emitted = 0
#     acks = 0
#     pongs = 0
    
#     def rx(self):
#         res = choice([Command.PING, Command.ABORT])
#         if res == Command.PING:
#             self.ping_emitted += 1
#         else:
#             self.normal_emitted += 1

#         return Message(res)

#     def tx(self, msg: Message):
#         if msg.command == Command.PONG:
#             self.pongs += 1
#         elif msg.command == Command.ACK:
#             self.acks += 1

# def test_dispatcher_ack_ping():
#     poll_ack = PhonyPollableAck()

#     # The PhonyPollableAck acts as a PING source, so only send PONGs
#     ack = AckPing(send_pings=False)

#     dispatcher = Dispatcher()
#     dispatcher.start()
#     dispatcher.subscribe_station(ack.rx, ack.command_set)
#     dispatcher.watch(poll_ack)

#     sleep(0.1)

#     ack.stop()
#     dispatcher.unwatch(poll_ack)
#     dispatcher.unsubscribe_station(ack.rx, ack.command_set)
#     dispatcher.stop()

#     assert 0 < poll_ack.pongs <= poll_ack.ping_emitted
#     assert 0 < poll_ack.acks <= poll_ack.normal_emitted
