#
#   Description: This file is used for testing the orbital_coms library
#


#  Expected Output:
#
# -----------------------------------------------------------------------
# Getters/Setters Test
# -----------------------------------------------------------------------
# test
# 62
# 30.3480N, 95.7827W
# 21
# -----------------------------------------------------------------------
# Special Functions Test
# -----------------------------------------------------------------------
# [*] Transmitting values...
# [!] Transmited!
# ABORT
# [*] Transmitting values...
# [!] Transmited!
# CUT
# -----------------------------------------------------------------------
# On-Call Functions Test
# -----------------------------------------------------------------------
# I have been summoned!


# This function is for testing command calls



import gs
import threading

g = gs.gs(True)

def abort():
    print("Uh Oh...")


def summon():
    return

def blank():
    return

#-------------------------------------------------------------------------------
# test gs
#-------------------------------------------------------------------------------
print("-----------------------------------------------------------------------")
print("GS Test")
print("-----------------------------------------------------------------------")

# get defualt values for testing
print(g.get_temperature())
print(g.get_location())
print(g.get_pressure())


#-------------------------------------------------------------------------------
# test gs in running mode
#-------------------------------------------------------------------------------

# subscribe events to functions
g.subscribe(gs.Event.LOCATION,abort)


threading.Thread(target=g.start).start()

def menu():
    print('''
    1. Send Abort
    2. Send Launch
    3. Send Cut
    4. Print All set Values
    5+. Exit
    ''')
    inp = input("Enter command-> ")

    if inp == "1":
        g.send_abort()
    elif inp == "2":
        g.send_launch()
    elif inp == "3":
        g.send_cut()
    elif inp == "4":
        print("""
Location:       {}
Temperature:    {:.2f}
Pressure:       {:.2f}
""".format(g.get_location(),float(g.get_temperature()),float(g.get_pressure())))
    else:
        exit()

while True:
    menu()
