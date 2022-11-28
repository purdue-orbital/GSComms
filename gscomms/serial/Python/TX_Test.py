import Serial

s = Serial.Serial()

while True:
    s.TX("pi")
    print("Sent!")
