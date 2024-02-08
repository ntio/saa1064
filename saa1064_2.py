import smbus
import time

bus = smbus.SMBus(1)
addr = 0x38

bus.write_byte_data(addr,0x00,0x17)

segments = {'dp': 0x01, 'a': 0x20, 'b': 0x10, 'c': 0x04, 'd': 0x02, 'e': 0x80, 'f': 0x40, 'g': 0x08}
numbers = {
	0: segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['e'] + segments['f'],
	1: segments['b'] + segments['c'],
	2: segments['a'] + segments['b'] + segments['g'] + segments['d'] + segments['e'],
	3: segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['g'],
	4: segments['b'] + segments['c'] + segments['g'] + segments['f'],
	5: segments['c'] + segments['d'] + segments['g'] + segments['a'] + segments['f'],
	6: segments['f'] + segments['e'] + segments['d'] + segments['c'] + segments['g'],
	7: segments['c'] + segments['b'] + segments['a'],
	8: segments['a'] + segments['b'] + segments['c'] + segments['d'] + segments['e'] + segments['f'] + segments['g'],
	9: segments['a'] + segments['b'] + segments['c'] + segments['f'] + segments['g']
}
i = 6
while True:
	print (i)	
	bus.write_byte_data(addr,0x01,numbers[i])
	time.sleep(1)
	bus.write_byte_data(addr,0x01,0x00)
