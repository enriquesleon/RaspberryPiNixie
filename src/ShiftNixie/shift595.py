#python module to interact with the HC595 SIPO shift registers


#Major Thanks to www.smbaker.com for his great shift register example

#	
#
#     16 15 14 13 12 11 10 09
#   |--|--|--|--|--|--|--|--|--|
#   |                          |
#   |         SN74HC595        |
#   |                          |
#   |--|--|--|--|--|--|--|--|--|
#     01 02 03 04 05 06 07 08
#
#
#
#   01	Output 1
#   02	Output 2
#   03	Output 3
#   04	Output 4
#   05  Output 5
#   06	Output 6
#   07	Output 7
#   08 	Ground
#   09	Overflow
#   10	CLR'
#   11	Serial Clock
#   12	Latch Clock
#   13	Output Enable'
#   14	Serial Input
#   15	Output 0
#   16	VCC

import RPi.GPIO as GPIO
import time
from   collections import deque
PIN_SERIAL = 29
PIN_ENABLE = 31
PIN_LATCH  = 33
PIN_CLK    = 35
PIN_CLR    = 37
DELAY      = .005
class Shift595:
	def __init__(self,serial = PIN_SERIAL,enable = PIN_ENABLE,latch = PIN_LATCH,clock = PIN_CLK,clear = PIN_CLR,number_registers = 3):
		self.serial_pin = serial
		self.enable_pin = enable
		self.latch_pin = latch
		self.clock_pin = clock
		self.clear_pin = clear
		self.number_registers = number_registers
		self.register_values = deque([0 for x in range(number_registers)],number_registers)
		#set up output for board Raspberry Pi board pin layout
		GPIO.setmode(GPIO.BOARD)

		#set pins for ouput
		GPIO.setup(self.serial_pin,GPIO.OUT)
		GPIO.setup(self.enable_pin,GPIO.OUT)
		GPIO.setup(self.latch_pin,GPIO.OUT)
		GPIO.setup(self.clock_pin,GPIO.OUT)
		GPIO.setup(self.clear_pin,GPIO.OUT)

		#setting default state. Then clear any data with clear pin

		GPIO.output(self.serial_pin,False)
		GPIO.output(self.enable_pin,False)
		GPIO.output(self.latch_pin,False)
		GPIO.output(self.clock_pin,False)
		GPIO.output(self.clear_pin,False)
		GPIO.output(self.clear_pin,True)
	#Delay to aid in propagation
	def delay(self):
		"This function adds a small delay to allow proper propagation"
		time.sleep(DELAY)

	#move values from shift registers into output registers
	def latch(self):
		"Latches in Values to the output registers"
		GPIO.output(self.latch_pin,True)
		self.delay()
		GPIO.output(self.latch_pin,False)
		self.delay()
	#loads serial logic value from Serial Pin into register 0 and shifts all following values. overflow outputs to q'
	def clock(self):
		GPIO.output(self.clock_pin,True)
		self.delay()
		GPIO.output(self.clock_pin,False)
		self.delay()
	#sets logic level of Serial Pin and sets one clock cycle to load in value to register 0	
	def shift_Bit(self,value):
		GPIO.output(self.serial_pin,value)
		self.delay()
		self.clock()
	#shifts in the least significant 8 bits of this value. From those 8 bits, the most significant bit is shifted first
	def shift_Value(self,value):
		Msb = 0x80
		self.register_values.appendleft(value&0xFF)
		print "{0:08b} {1}".format(value&0xFF,int(value))

		for x in range(8):
			self.shift_Bit((value<<x)&Msb)

	def shift_All(self,values = [0]):
		for x in values:
			self.shift_Value(x)
		self.latch()
	def current_Values(self):
		return self.register_values
	def clean_Up(self):
		GPIO.cleanup()
def debug_Shift(number_registers):
	shift = Shift595()
	return shift

def main():
	shift = Shift595()
	#test pattern for nixie tube of 0 1 2 3 4 5
	shift.shift_All([1,35,69])
	GPIO.cleanup()
if __name__ == '__main__':
	main()





