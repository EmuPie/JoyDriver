#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

# Adapted for <insert ADC name here> by Rickard Doverfelt

import time
import os
import RPi.GPIO as GPIO
import evdev
import evdev.eventio.EventIO as EventIO
from evdev import UInput, InputDevice, categorize, ecodes
dev = UInput(None, 'py-evdev-uinput', 1, 1, 3, '/dev/input/event0')

GPIO.setmode(GPIO.BCM)

# read SPI data from <insert ADC name here> chip, 4 possible adc's (0 thru 3)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 3) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = 0
	
	if (adcnum == 0):
		commandout = 12
	elif (adcnum == 1):
		commandout = 14
	elif (adcnum == 2):
		commandout = 13
	elif (adcnum == 3):
		commandout = 15

        commandout <<= 4    # we only need to send 4 bits here
        for i in range(4):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Pi
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# The channel number for each axis
joyX1 = 0
joyY1 = 1
joyX2 = 2
joyY2 = 3

isW = False
isS = False
isA = False
isD = False

isUp = False
isDown = False
isLeft = False
isRight = False

while True:
	
	# Do the input logic
	if (readadc(joyX, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		if (isA != True):
			dev.write(e.EV_KEY, e.KEY_A, 1)
			isA = True
	else:
		if (isA == True):
			dev.write(e.EV_KEY, e.KEY_A, 0)
			isA = False
	
	if (readadc(joyX1, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		if (isD != True):
			dev.write(e.EV_KEY, e.KEY_D, 1)
			isD = True
	else:
		if (isD == True):
			dev.write(e.EV_KEY, e.KEY_D, 0)
			isD = False

	if (readadc(joyY1, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		if (isS != True):
			dev.write(e.EV_KEY, e.KEY_S, 1)
			isS = True
	else:
		if (isS == True):
			dev.write(e.EV_KEY, e.KEY_S, 0)
			isS = False
	
	if (readadc(joyY1, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		if (isW != True):
			dev.write(e.EV_KEY, e.KEY_W, 1)
			isW = True
	else:
		if (isW == True):
			dev.write(e.EV_KEY, e.KEY_W, 0)
			isW = False

	if (readadc(joyX2, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		if (isLeft != True):
			dev.write(e.EV_KEY, e.KEY_LEFT, 1)
			isLeft = True
	else:
		if (isLeft == True):
			dev.write(e.EV_KEY, e.KEY_LEFT, 0)
			isLeft = False
	
	if (readadc(joyX2, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		if (isRight != True):
			dev.write(e.EV_KEY, e.KEY_RIGHT, 1)
			isRight = True
	else:
		if (isRight == True):
			dev.write(e.EV_KEY, e.KEY_RIGHT, 0)
			isRight = False

	if (readadc(joyY2, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		if (isDown != True):
			dev.write(e.EV_KEY, e.KEY_DOWN, 1)
			isDown = True
	else:
		if (isDown == True):
			dev.write(e.EV_KEY, e.KEY_DOWN, 0)
			isDown = False
	elif (readadc(joyY2, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		if (isUp != True):
			dev.write(e.EV_KEY, e.KEY_UP, 1)
			isUp = True
	else:
		if (isUp == True):
			dev.write(e.EV_KEY, e.KEY_UP, 0)
			isUp = False

