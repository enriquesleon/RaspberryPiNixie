#This is the Nixie Display module that will be used that provides a high level interface 
#to the Shift Registers and the Nixie Tube Display. Users should provide the number of
#tubes in the display in the constructor. Updating the display involves loading the update method 
#with an array of integers that the tube will display. If the value is out of range, the value will
#default to zero in order to avoid blanking the tubes and damaging them. The left most
#value in the array will be shifted first.
import shift595
import time
import math
import RPi.GPIO as GPIO
PIN_SERIAL = 29
PIN_ENABLE = 31
PIN_LATCH  = 33
PIN_CLK    = 35
PIN_CLR    = 37
DELAY      = .010
LSByte 	   = 0x0F 	
class NixieDisplay:
	class NixieTube:
		def __init__(self):
			self.half_Byte_Value = 0

		def current_value(self):
			return self.half_Byte_Value
		def blank(self):
			self.half_Byte_Value = 0x0F
		def set_value(self,n_value):
			if n_value > 9:
				n_value = 9
			self.half_Byte_Value = n_value

	def __init__(self,number_Displays,shift):
		"Class Requires an instance of the Shift595 class in order to operate on the shift registers"
		self.number_Displays = number_Displays
		self.number_Registers = int(math.ceil(self.number_Displays/2))
		
		if self.number_Displays%2 != 0:
			self.half_Bytes = self.number_Displays +1
		else:
			self.half_Bytes = self.number_Displays

		self.nixie_tubes = [self.NixieTube() for i in range(self.half_Bytes)]
		self.shift = shift
		self.currentValues = self.shift.register_values
		self.span = [i*2 for i in range(self.half_Bytes//2)]
	
	def update(self):
		"Call this method anytime you wish to update the values on the display from the loaded string"
		grouped_Values = [[self.get_display_value(j),self.get_display_value(j+1)] for j in self.span]
		print "Grouped Register Values: {}".format(grouped_Values)
		combined_Values = [self.__combine_To_Register(values) for values in grouped_Values]
		self.shift.shift_All(combined_Values)

	def __combine_To_Register(self,display_Value = [0,0]):
		"Private method. Don't touch. Combines two hex values into a number that can be loaded into a register"
		most_SigReg_HByte  = display_Value[0]&LSByte
		least_SigReg_HByte = display_Value[1]&LSByte
		most_SigReg_HByte  = most_SigReg_HByte << 4

		registerValue = most_SigReg_HByte|least_SigReg_HByte
		print "Most: {} Least: {} Register: {}".format(most_SigReg_HByte>>4,least_SigReg_HByte,registerValue)

		return registerValue
	
	def clear_display(self):
		"Sets all values in the display to zero"
		for tube in self.nixie_tubes:
			tube.set_value(0x0)
	def set_display(self,index,value):
		'''Set a particular tube to the given value. Display remains unchanged if string cannot be cast into an int'''
		try:
			self.nixie_tubes[index].set_value(int(value))
		except ValueError as ve:
			print "Invalid Type Input for {}".format(value)
	def get_display_value(self,index):
		return self.nixie_tubes[index].current_value()
	def blink(self,times = 0,time = 0 ,delay = 10000):
		pass	
	
	def string_display(self,output_string):
		"""Pass in a number string to display on the nixie display. If the string length is less than the number of tubes,
		the rest of the display will display zero. If the string is to long, only the length of number of of displays numbers will be shown.
		"""
		if len(output_string) > self.number_Displays:
			output_string = output_string[:self.number_Displays]
		if len(output_string) < self.number_Displays:
			output_string = output_string + ("0"*(self.number_Displays-(len(output_string))))
		digits = [digit for digit in output_string]
		for i in range(len(output_string)):
			self.set_display(i,digits[i])
def main():
	shift = shift595.Shift595()
	display = NixieDisplay(6,shift)
	while True:
		d_string = raw_input()
		display.string_display(d_string)
		display.update()
if __name__ == '__main__':
	main()




	
