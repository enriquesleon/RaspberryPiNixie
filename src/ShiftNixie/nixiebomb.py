#clock test for nixie tube clock
import nixiedisplay
import shift595
import time

display = nixiedisplay.NixieDisplay(4,shift595.Shift595())

def countdown(n):
	while n > 0:
		string = "%d" % n
		display.string_display(string)
		display.update()
		n -= 1
		time.sleep(1)

def main():
	countdown(9999)

if __name__ == '__main__':
	main()
