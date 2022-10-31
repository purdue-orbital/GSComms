import Serial

s = Serial.Serial()
l = s.RX()
print("00110001" in l)
