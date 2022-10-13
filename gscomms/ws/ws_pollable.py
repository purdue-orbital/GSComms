import websocket

from gscomms.common.message import Message


class WsPollable:
    def __init__(self, address: str):
        self.ws = websocket.WebSocketApp(address, on_message=self.on_message)
        self.ws.run_forever()

        self.received_msgs_queue = []

    def on_message(self, app, msg):
        self.received_msgs_queue.append(Message.deserialize(msg))

    def tx(self, msg: Message):
        self.ws.send(msg.serialize())

    def rx(self):
        if len(self.received_msgs_queue) == 0:
            return None
        return self.received_msgs_queue.pop(0)

    def stop(self):
        self.ws.close()
