#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

debug = True

def debug_print(my_line,must_print = False):
    if debug or must_print:
        print my_line

# Pring X dots with Y seconds delay between dots
def print_X_dots(numberOfSymbols,sleepTiem,printSymbole="."):
    print("\n")
    for n in range(0, numberOfSymbols):
        print(printSymbole)
        time.sleep( 5 )
    print("\n")


