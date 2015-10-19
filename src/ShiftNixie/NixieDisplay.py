#This is the Nixie Display module that will be used that provides a high level interface 
#to the Shift Registers and the Nixie Tube Display. Users should provide the number of
#tubes in the display in the constructor. Updating the display involves loading the update method 
#with an array of integers that the tube will display. If the value is out of range, the value will
#default to zero in order to avoid blanking the tubes and damaging them. The left most
#value in the array will be shifted first.
#import shift595
import time
import math
#import RPi.GPIO as GPIO
PIN_SERIAL = 29
PIN_ENABLE = 31
PIN_LATCH  = 33
PIN_CLK    = 35
PIN_CLR    = 37
DELAY      = .010
LSByte 	   = 0x0F 	
class NixieDisplay:
	def __init__(self,dNumber_Displays):
		self.number_displays = number_displays
		self.numberRegisters = int(math.ceil(self.number_displays/2))
		self.shift = shift595(PIN_SERIAL,PIN_ENABLE,PIN_LATCH,PIN_CLK,PIN_CLR,self.numberRegisters)
		self.currentValues = shift.register_values
	def updateDisplay(self,dValuesList = [0]):
		pass
	def combineToRegister(self,dRegisterValue = [0,0]):
		mostSigRegByte  = dRegisterValue[0]&LSByte
		leastSigRegByte = dRegisterValue[1]&LSByte
		mostSigRegByte  = mostSigRegByte << 4
		registerValue = mostSigRegByte|leastSigRegByte
		return registerValue



	
