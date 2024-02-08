from __future__ import print_function
import time
import platform
import smbus



class SevenSegmentDisplay:
    MAX_DIGITS = 4
    SAA1064_CONTROL_REG_ADDRESS = 0x00
    SAA1064_CONTROL_DEFAULT = 0x17    # Dynamic mode,1+3 & 2+4 not blanked, 3mA segment current only
    
    def __init__(self, address, digit_map, i2cBusId=1, debug=0):
        
        self.address = address # address of display
        self.digit_map = digit_map  # the mapped ordering of 7 segment digits
        self.current_digit_seqment_values = [0, 0, 0, 0]
        self.number_digits_displaying_something = 0
        self.debug_print = debug
        self.bus = smbus.SMBus(i2cBusId)
      
        
        self.bus.write_byte_data(address, self.SAA1064_CONTROL_REG_ADDRESS, self.SAA1064_CONTROL_DEFAULT)
    
    def __repr__(self):
        """return string representation"""
        return "Display Address = 0x{:02x}, Display Map = {}".format(self.address, self.digit_map )
        
    # This function clears all the digits
    def clear_all_digits(self):
        # clear all digits
        for n in range (1, self.MAX_DIGITS + 1):
            self.clear_digit(n)
        self.current_digit_seqment_values = [0, 0, 0, 0]
        self.number_digits_displaying_something = 0

    def reset_device(self):
        self.bus.write_byte_data(self.address,0x00,0x17)
        
    def clear_digit(self, digit_to_clear):
        self.bus.write_byte_data(self.address, self.digit_map[digit_to_clear-1], 0x00)
    
    def update_digit(self, digit, value, dp=0):
        
        if(digit <= self.MAX_DIGITS):
            try:
                if(dp == 0):
                    new_value = numbers[value]
                else: 
                    new_value = numbers[value] + numbers[dp]
            except (KeyError):
                new_value = 0 
            
            if(new_value != self.current_digit_seqment_values[digit-1]):	
                self.bus.write_byte_data(self.address,self.digit_map[digit-1],new_value)
                self.current_digit_seqment_values[digit-1] = new_value
        else:
            if self.debug_print:
                print ("digit max exceeded {}".format(digit))
    
    def write_number(self, value):
        #time.sleep(0.8)
        if(type(value) is str):
            self.write_str_number(value)
        elif(type(value) is int):  
            self.write_int(value)
        elif(type(value) is float):
            self.write_float(value)
        else:
            raise ValueError("Can't write Non handled type")

    def write_int(self, value):
        if(value > 9999):
            value = 9999
        if(value < -999):
            value = -999
        num_as_string = str(value)
        length = len(num_as_string)
        digitCount = 1 
        while (length):
            self.update_digit(digitCount, num_as_string[length-1])
            digitCount += 1
            length -= 1    

    def write_float(self, value):
        if(value > 999.9):
            value = 999.9
        if(value < 0.0):
            value = 0.0
        num_as_string = str(value)
        self.write_str_number(num_as_string)
    

    def write_str_number(self, value):
        num_as_string = str(value)
        dp_flag = False
        digitCount = 1
        
        calcDigit = self.calcDigitsRequired(num_as_string)
        if(calcDigit < self.number_digits_displaying_something):
            self.clear_all_digits()
        self.number_digits_displaying_something = calcDigit
        
        for i, char in reversed(list(enumerate(num_as_string))):
            if(char =='.'):
                if(i==0 or num_as_string[i-1]=='.'): # if this is last character or if next digit is "dp" 
                    self.update_digit(digitCount," ","DP")
                    digitCount += 1
                else:
                    dp_flag = True # appy DP to next digit
            else:
                if(dp_flag == True):
                    self.update_digit(digitCount,char,"DP")
                    dp_flag = False
                else:
                    self.update_digit(digitCount,char)
                digitCount += 1
                
    def calcDigitsRequired(self,string):
        """Works out how many digits would be effected/required if the string was to be printed"""
        digitsRequired = 0
        for i, char in reversed(list(enumerate(string))):
            if(char =='.'):
                if(i==0 or string[i-1]=='.'): # if this is last character or if next digit is "dp" 
                    digitsRequired += 1
            else:
                digitsRequired += 1
        return digitsRequired
                
segments = {'dp': 0x01, 'a': 0x20, 'b': 0x10, 'c': 0x04, 'd': 0x02, 'e': 0x80, 'f': 0x40, 'g': 0x08}
#{'dp': 0x01, 'a': 0x02, 'b': 0x04, 'c': 0x08, 'd': 0x10, 'e': 0x20, 'f': 0x40, 'g': 0x80}

numbers = {
    ' ': 0x00,
    'DP': segments['dp'],
    '0': segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['e'] + segments['f'],
    '1': segments['b'] + segments['c'],
    '2': segments['a'] + segments['b'] + segments['g'] + segments['e'] + segments['d'],
    '3': segments['a'] + segments['b'] + segments['g'] + segments['c'] + segments['d'],
    '4': segments['f'] + segments['g'] + segments['b'] + segments['c'],
    '5': segments['c'] + segments['d'] + segments['g'] + segments['a'] + segments['f'],
    '6': segments['c'] + segments['d'] + segments['e'] + segments['f'] + segments['g'] + segments['a'],
    '7': segments['c'] + segments['b'] + segments['a'],
    '8': segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['e'] + segments['f'] + segments['g'],
    '9': segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['f'] + segments['g'],
    'A': segments['a'] + segments['b'] + segments['c'] + segments['e'] + segments['f'] + segments['g'],
    'b': segments['c'] + segments['d'] + segments['e'] + segments['f'] + segments['g'],
    'C': segments['a'] + segments['d'] + segments['e'] + segments['f'],
    'd': segments['b'] + segments['c'] + segments['d'] + segments['e'] + segments['g'],
    'E': segments['a'] + segments['d'] + segments['e'] + segments['f'] + segments['g'],
    'F': segments['a'] + segments['e'] + segments['f']+ segments['g'],
    'r': segments['e'] + segments['g'],	
    '-': segments['g'],
    '+': segments['g'] + segments['b']
}

