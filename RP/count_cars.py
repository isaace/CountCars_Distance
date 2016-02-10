#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General imports
import RPi.GPIO as GPIO
import utils as u
import time

def distance(GPIO_ECHO,GPIO_TRIG):
    u.debug_print ("GPIO_TRIG = " + str(GPIO_TRIG) + ",GPIO_ECHO = " + str(GPIO_ECHO))
    # Set GPIO Channels
    # -----------------
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_TRIG, GPIO.OUT)
    GPIO.output(GPIO_TRIG, False)


    # A couple of variables
    # ---------------------
    EXIT = 0                        # Infinite loop
    decpulsetrigger = 0.0001        # Trigger duration
    inttimeout = 1000               # Number of loop iterations before timeout called


    # Wait for 2 seconds to allow the ultrasonics to settle (probably not needed)
    # ---------------------------------------------------------------------------
    #print "Waiting for 2 seconds....."
    #time.sleep(2)


    # Go
    # --
    u.debug_print("Running....")
    min_dist = 100

    # Never ending loop
    # -----------------
    while EXIT < 10:

        # Trigger high for 0.0001s then low
        GPIO.output(GPIO_TRIG, True)
        time.sleep(decpulsetrigger)
        GPIO.output(GPIO_TRIG, False)

        # Wait for echo to go high (or timeout)
        i_countdown = inttimeout

        while (GPIO.input(GPIO_ECHO) == 0 and i_countdown > 0):
            i_countdown -=  1

        # If echo is high than the i_countdown not zero
        if i_countdown > 0:

            # Start timer and init timeout countdown
            echostart = time.time()
            i_countdown = inttimeout

            # Wait for echo to go low (or timeout)
            while (GPIO.input(GPIO_ECHO) == 1 and i_countdown > 0):
                i_countdown -= 1

            # Stop timer
            echoend = time.time()


            # Echo duration
            echoduration = echoend - echostart

        # Display distance
        if i_countdown > 0:
            i_distance = (echoduration*1000000)/58
            u.debug_print("Distance = " + str(i_distance) + "cm")
            min_dist = min(min_dist,i_distance)
        else:
            u.debug_print("Distance - timeout")

            # Wait at least .01s before re trig (or in this case .1s)
            time.sleep(.1)

        EXIT +=1
        return min_dist


# Which GPIO's are used [0]=BCM Port Number [1]=BCM Name [2]=Use [3]=Pin
# ----------------------------------------------------------------------
GPIO_ECHO = 21
GPIO_TRIG = 20

#Global defines
sleep_const = 2.5 #sleep period between each sampling

#__main__
u.debug_print("Hello WeroJam")

while 1:
    print("Start counting\n")
    curDist = distance(GPIO_ECHO,GPIO_TRIG)
    print("curDist is " + str(curDist) + "cm.\n")
    u.debug_print("sleeping for " + str(sleep_const) +  " seconds\n",True)
    time.sleep(sleep_const)
