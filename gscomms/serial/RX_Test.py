from .Serial import *


#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

rx_sample_rate = 4e6 # Freqency at which the radio samples waves
freqency       = 915e6 # Freqency at which the radio will read
sample_size    = int(4e6) # Number of data points to collect
num_data       = 100 # Number of data points to be displayed on the graph





s = Serial(freqency,freqency,0,0,20,20)
s.connect()

time.sleep(1)

while True:
    arr = s.rx()

print(arr)

s.disconnect()
