from __future__ import print_function

import argparse

parser = argparse.ArgumentParser(description='i2c display class tester')

parser.add_argument('-d','--displayID', default=2, type=int, help='the display ID/number to use')
parser.add_argument('--countUp',action="store_true", help='The count up switch')
parser.add_argument('-c','--countVal', default=9999, type=int, help='The count start value')
parser.add_argument('-i','--interactive', action="store_true", help='Interactive mode')

args = parser.parse_args()

#print ("displayID is {}".format(args.displayID))
#print ("countUp is {}".format(args.countUp))
#print ("countVal is {}".format(args.countVal))

#exit()

import platform
from saa1064driver import SevenSegmentDisplay

import time
import sys

usleep = lambda x: time.sleep(x/1000000.0)
msleep = lambda x: time.sleep(x/1000.0)

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

QuadAddressMap = [0x38,0x39,0x3a,0x3b]

QuadDigitMap =[[1, 2, 3, 4],[1, 2, 4, 3],[1, 2, 3, 4],[1, 2, 3, 4]]

terminalValue = args.countVal

quadToUse = num(args.displayID)

addressToUse = 0x38 #QuadAddressMap[quadToUse -1]	
QuadDigitMapToUse = [1, 2, 3, 4] #QuadDigitMap[quadToUse -1]

display_group1 = SevenSegmentDisplay(addressToUse, QuadDigitMapToUse) 

def countdown(number,countUp=False):
    prevTime = time.time()
    delta = 0
    
    if countUp:
        print ("Up Counting...")
        initialValue = 0
        increment = +1
        terminalValue = number
    else:
        print ("Down Counting...")    
        initialValue = number + 1
        increment = -1
        terminalValue = -1
    
    for x in range(initialValue,terminalValue, increment):
        display_group1.write_str_number(x)
        while(delta <= 0.1):
            delta = time.time() - prevTime
        prevTime = time.time()
        delta = 0

display_group1.reset_device()	
display_group1.clear_all_digits()	

if (args.interactive):
    print ("interactive mode")
    number = input("Enter value:")
    while (number != "9999"):
        display_group1.write_number(number)
        number = input("Enter value:")
else:
    countdown(int(terminalValue),args.countUp)
exit()



