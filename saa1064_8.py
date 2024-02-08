'''Seven segment display of hex digits.'''

#import tkinter as tk
from tkinter import *
import platform
import time
from saa1064driver import SevenSegmentDisplay
import smbus


root = Tk()
screen = Canvas(root)
screen.grid()


# Order 7 segments clockwise from top left, with crossbar last.
# Coordinates of each segment are (x0, y0, x1, y1) 
# given as offsets from top left measured in segment lengths.
offsets = [
    ( # digit 4 (left most)
    (0, 0, 1, 0),  # a segment
    (1, 0, 1, 1),  # b segment
    (1, 1, 1, 2),  # c segment
    (0, 2, 1, 2),  # d segment
    (0, 1, 0, 2),  # e segment
    (0, 0, 0, 1),  # f segment
    (0, 1, 1, 1),  # g segment
    (1.1,2.1,1.3,2.3) # DP
    ),
    (# digit 3
    (2+0, 0, 2+1, 0),  # a segment
    (2+1, 0, 2+1, 1),  # b segment
    (2+1, 1, 2+1, 2),  # c segment
    (2+0, 2, 2+1, 2),  # d segment
    (2+0, 1, 2+0, 2),  # e segment
    (2+0, 0, 2+0, 1),  # f segment
    (2+0, 1, 2+1, 1),  # g segment
    (2+1.1,2.1,2+1.3,2.3) # DP
    ),
    (# digit 2
    (4+0, 0, 4+1, 0),  # a segment
    (4+1, 0, 4+1, 1),  # b segment
    (4+1, 1, 4+1, 2),  # c segment
    (4+0, 2, 4+1, 2),  # d segment
    (4+0, 1, 4+0, 2),  # e segment
    (4+0, 0, 4+0, 1),  # f segment
    (4+0, 1, 4+1, 1),  # g segment
    (4+1.1,2.1,4+1.3,2.3) # DP
    ),
    (# digit 1 (right most)
    (6+0, 0, 6+1, 0),  # a segment
    (6+1, 0, 6+1, 1),  # b segment
    (6+1, 1, 6+1, 2),  # c segment
    (6+0, 2, 6+1, 2),  # d segment
    (6+0, 1, 6+0, 2),  # e segment
    (6+0, 0, 6+0, 1),  # f segment
    (6+0, 1, 6+1, 1),  # g segment
    (6+1.1,2.1,6+1.3,2.3) # DP
    )
    ]      

class Digit:
    def __init__(self, canvas, address_of_display, x=10, y=10, length=20, width=4):
        self.canvas = canvas
        self.addressOfI2C_Simulator = address_of_display
        self.bus = smbus.SMBus(1)
        l = length
        self.segs = [[],[],[],[]]
        for index, sevenSeg in enumerate(offsets):
            for x0, y0, x1, y1 in sevenSeg:
                self.segs[index].append(canvas.create_line(
                    x + x0*l, y + y0*l, x + x1*l, y + y1*l,
                    width=width, state = 'hidden',fill='red'))
   
    def show_i2c(self):
        segmentList1 = self.generateDigitSegmentList(self.bus.read_byte_data(self.addressOfI2C_Simulator,1))
        segmentList2 = self.generateDigitSegmentList(self.bus.read_byte_data(self.addressOfI2C_Simulator,2))
        segmentList3 = self.generateDigitSegmentList(self.bus.read_byte_data(self.addressOfI2C_Simulator,3))
        segmentList4 = self.generateDigitSegmentList(self.bus.read_byte_data(self.addressOfI2C_Simulator,4))
        
        for iid, on in zip(self.segs[0], segmentList1):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')
        for iid, on in zip(self.segs[1], segmentList2):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')
        for iid, on in zip(self.segs[2], segmentList3):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')
        for iid, on in zip(self.segs[3], segmentList4):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')

    def generateDigitSegmentList(self,value):
        return [(value & 0x02)== 0x02,(value & 0x04)== 0x04,(value & 0x08)== 0x08,(value & 0x10)== 0x10,
                (value & 0x20)== 0x20,(value & 0x40)== 0x40,(value & 0x80)== 0x80,(value & 0x01)== 0x01]



QuadAddressMap = [0x38,0x39,0x3a,0x3b]

QuadDigitMap =[[1, 2, 3, 4],[2, 1, 4, 3],[4, 3, 2, 1],[1, 2, 3, 4]]

quadToUse = 3
addressToUse =  0x38 # QuadAddressMap[quadToUse-1]    
QuadDigitMapToUse = [1, 2, 3, 4] #QuadDigitMap[quadToUse-1]

simulatedDisplay = Digit(screen,addressToUse)
timebase = 1
n = 0
#display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse)
def update():
    global n
   
    if(timerShowValue.get()):
        display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse,debug=False)
        display1.write_number(n) 

        
    simulatedDisplay.show_i2c()
    n = (n + 1) % 9999
        
    root.after(timebase, update)

def write_time_delta():
    global n
    global lastTime
    currentTime = time.time()
    delta = currentTime - lastTime 
    delta_str= "{:02.1f}".format(delta)
    lastTime = currentTime
    display1 = SevenSegmentDisplay(addressToUse,QuadDigitMapToUse,debug=False)
    if(timerShowValue.get() == 0):
        display1.write_number(value.get()) 
    print("Last Pressed {:02.1f} seconds ago. {}".format(delta,value.get()))
   

lastTime = time.time()

timerShowValue = IntVar()
checkbox = Checkbutton(screen, text="Use timebase", variable=timerShowValue)
checkbox.place(relx=.80, rely=.5, anchor="c")
#checkbox.var = timerShowValue

value = StringVar()
editbox = Entry(screen, textvariable=value)
value.set("1.1.1.2")
editbox.place(relx=.30, rely=.5, anchor="c")

slogan = Button(screen,text="Update", command=write_time_delta)
slogan.place(relx=.55, rely=.5, anchor="c")

root.after(timebase, update())
root.mainloop()

