#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import RPi.GPIO as GPIO
import uinput

device = uinput.Device([
	uinput.KEY_W,
	uinput.KEY_S,
	uinput.KEY_A,
	uinput.KEY_D,
	uinput.KEY_UP,
	uinput.KEY_LEFT,
	uinput.KEY_DOWN,
	uinput.KEY_RIGHT
	])

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
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
	
        #commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 4    # we only need to send 5 bits here
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
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
joyX1 = 0
joyY1 = 1
joyX2 = 2
joyY2 = 3

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

while True:
	
	#print("X1: " + str(readadc(joyX1, SPICLK, SPIMOSI, SPIMISO, SPICS)))
	#print("Y1: " + str(readadc(joyY1, SPICLK, SPIMOSI, SPIMISO, SPICS)))
	#print("X2: " + str(readadc(joyX2, SPICLK, SPIMOSI, SPIMISO, SPICS)))
	#print("Y2: " + str(readadc(joyY2, SPICLK, SPIMOSI, SPIMISO, SPICS)))
	if (readadc(joyX1, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		device.emit_click(uinput.KEY_A)
	elif (readadc(joyX1, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		device.emit_click(uinput.KEY_D)

	if (readadc(joyY1, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		device.emit_click(uinput.KEY_S)
	elif (readadc(joyY1, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		device.emit_click(uinput.KEY_W)

	if (readadc(joyX2, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		device.emit_click(uinput.KEY_LEFT)
	elif (readadc(joyX2, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		device.emit_click(uinput.KEY_RIGHT)

	if (readadc(joyY2, SPICLK, SPIMOSI, SPIMISO, SPICS) < 924):
		device.emit_click(uinput.KEY_DOWN)
	elif (readadc(joyY2, SPICLK, SPIMOSI, SPIMISO, SPICS) > 1124):
		device.emit_click(uinput.KEY_UP)

