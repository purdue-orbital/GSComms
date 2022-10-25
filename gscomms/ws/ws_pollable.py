import socket
import threading
from time import sleep
from typing import Callable
import websocket

from common.message import Message
from common.dispatcher import Dispatcher


class WsPollable:
    def __init__(self, address: str):
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # s.connect(("127.0.0.1", 8081))
        self.received_msgs_queue = []
        self.run_thread = True
        self.hnd = None

        self.ws = websocket.WebSocketApp(address, on_message=self.on_message, on_open=lambda _: print('connected'))

        self.ws_hnd = threading.Thread(target = self.ws.run_forever)
        self.ws_hnd.start()

    def on_subscribed(self, pop: Callable):
        def thread_func():
            while self.run_thread:
                if val := pop():
                    self.ws.send(val.serialize())
                sleep(50 / 1000)

        self.hnd = threading.Thread(target=thread_func)
        self.hnd.start()

    def on_message(self, app, msg):
        deserialized = Message.deserialize(msg)
        print(f'Received message: {deserialized.to_string()}')
        Dispatcher().push_stations(deserialized)

    def stop(self):
        self.run_thread = False
        if hnd := self.hnd:
            if hnd.is_alive():
                hnd.join()
        self.ws.close()
        self.ws_hnd.join()
