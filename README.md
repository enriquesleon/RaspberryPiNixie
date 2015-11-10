# RaspberryPiNixie
SDSU 530
This is the source code for our CS530 NixieTube display project. Nixie tubes are a form of cold cathode display that can output digital numerals.This project involves setting up a Raspberry Pi to interface with a set of 3 SN74HC595 shift registers which allows 5 GPIO pins to control the output of the 24 pins on the shift registers. Each Register will control 2 Nixie tubes, 4 bits each. Each Nixie Tube will be driven by a k1551d Nixie Tube Driver IC that accepts 4 bits of input to ground one of 10 numerals of the display. This library contains a high level interface to the 595 type shift register with a customized amount of daisy chained registers. Also included is a high level interface to write a numerical string to display. A sample clock program is also provided as an example.
An over view of the K1551 chip can be found here:

http://neonixie.com/ic/english-datasheet-1.jpg

http://neonixie.com/ic/english-datasheet-2.jpg

Usage:

import nixiedisplay
import shift595

shift = shift595.Shift595()
display = nixiedisplay.NixieDisplay(6,shift)
display.string_display("123456")
display.update()
