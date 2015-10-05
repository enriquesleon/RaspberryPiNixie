# RaspberryPiNixie
SDSU 530
This is the source code for our CS530 NixieTube display project
and overview on nixie tube can be found here:https://en.wikipedia.org/wiki/Nixie_tube
This project involves setting up a Raspberry Pi to interface with a set of 3 SN74HC595 shift registers.
Each Register will control 2 Nixie tubes, 4 bits each. 
An Overview of the SN74HC595 IC can be found here: http://www.ti.com/lit/ds/symlink/sn74hc595.pdf
Each Nixie tube is controlled by one k1551 Nixie Tube driver chip which recieves a BCD from one of the HC595's to sink one cathode 
lead on the tube to light up that given digit.
An over view of the K1551 chip can be found here:
http://neonixie.com/ic/english-datasheet-1.jpg
http://neonixie.com/ic/english-datasheet-2.jpg
