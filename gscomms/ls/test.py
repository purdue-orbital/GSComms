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

import threading

# This function is for testing command calls
def summon():
    print("I have been summoned!")
def blank():
    return


import gscomms.ls.ls_old as ls_old
import threading
from gscomms.ls.logging import Log

l = ls_old.ls(True)

#-------------------------------------------------------------------------------
# test ls
#-------------------------------------------------------------------------------
print("-----------------------------------------------------------------------")
print("LS Test")
print("-----------------------------------------------------------------------")

l.send_temperature(62.0)
l.send_location("30.3480N, 95.7827W")
l.send_pressure(21.0)

Log("Test!")


threading.Thread(target=l.start).start()

def menu():
    print('''
    1. Send Temperature
    2. Send Location
    3. Send Pressure
    4+. Exit
    ''')
    inp = input("Enter command-> ")

    if inp == "1":
        tempe = float(input("Enter temperature-> "))
        l.send_temperature(tempe)
    elif inp == "2":
        loc = input("Enter location-> ")
        l.send_location(loc)
    elif inp == "3":
        pres = float(input("Enter pressure-> "))
        l.send_pressure(pres)
    else:
        exit()

while True:
    menu()
