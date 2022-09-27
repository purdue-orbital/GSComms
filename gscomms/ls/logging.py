from time import sleep

mux = False

def Log(data):
    global mux
    while mux:
        sleep(0.001)
    # prevent multi writes
    mux = True

    file = open("log.txt","a+")
    file.write(str(data)+"\n")
    file.close()

    # open file to writes
    mux = False
