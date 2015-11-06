#clock test for nixie tube clock
import nixiedisplay
import shift595
import time
def main():
	display = nixiedisplay.NixieDisplay(6,shift595.Shift595())
	last_time = time.localtime()
	last_second = last_time.tm_sec
	while True:
		time.sleep(.1)
		current_time = time.localtime()##"{}{}{}".format(*(time.localtime())[3:6])
		current_sec = current_time.tm_sec
		if current_sec != last_time.tm_sec:
			time_string = time.strftime("%H%M%S",time.localtime())
			print "Timestring: {}".format(time_string)
		  	display.string_display(time_string)
		  	display.update()
		  	last_time = current_time
if __name__ == '__main__':
	main()


