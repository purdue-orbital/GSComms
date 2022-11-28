import Serial
import threading
import time

s = Serial.Serial()

def tx_cycle():
    global s
    while True:
        s.TX('pi')
        time.sleep(0.8)


threading.Thread(target=tx_cycle).start()

while True:
    s.RX()
