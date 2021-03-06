#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General imports
import RPi.GPIO as GPIO
import utils as u
import time

def distance(GPIO_ECHO,GPIO_TRIG,cars=0,should_print=True):
    #u.debug_print ("GPIO_TRIG = " + str(GPIO_TRIG) + ",GPIO_ECHO = " + str(GPIO_ECHO))
    # Set GPIO Channels
    # -----------------
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_TRIG, GPIO.OUT)
    GPIO.output(GPIO_TRIG, False)


    # A couple of variables
    # ---------------------
    EXIT = 0                        # Infinite loop
    decpulsetrigger = 0.0001        # Trigger duration
    inttimeout = 2000               # Number of loop iterations before timeout called


    # Wait for 2 seconds to allow the ultrasonics to settle (probably not needed)
    # ---------------------------------------------------------------------------
    #print "Waiting for 2 seconds....."
    #time.sleep(2)


    # Go
    # --
    #u.debug_print("Running....")
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
            if i_distance < car_detection_trashold and should_print:
                u.debug_print("Car number " + str(cars+1) + " was detected at " + str(i_distance) + "cm")
            min_dist = min(min_dist,i_distance)
        else:
            #u.debug_print("Distance - timeout")

            # Wait at least .01s before re trig (or in this case .1s)
            time.sleep(0.05)

        EXIT +=1
        return min_dist


# Which GPIO's are used [0]=BCM Port Number [1]=BCM Name [2]=Use [3]=Pin
# ----------------------------------------------------------------------
GPIO_ECHO = 21
GPIO_TRIG = 20

#Global defines
sleep_const = 0.1 #sleep period between each sampling
green_light_interval = 5 #how long we will have the green light, in seconds
car_detection_trashold = 25#if the distance is less than the trashold than a car was detected


#__main__
u.debug_print("Hello Wer-O-Jam")

while 1:
    i = 0
    t_end = time.time() + green_light_interval
    print("Start counting\n")
    while time.time() < t_end:
        curDist = distance(GPIO_ECHO,GPIO_TRIG,i)
        #print("curDist is " + str(curDist) + "cm.\n")
        #u.debug_print("sleeping for " + str(sleep_const) +  " seconds\n",True)
        time.sleep(sleep_const/10)
        if curDist < car_detection_trashold:
            i+=1
            while curDist < car_detection_trashold:
                time.sleep(sleep_const)
                curDist = distance(GPIO_ECHO,GPIO_TRIG,i,False)
                u.debug_print("Inside loop")
            u.debug_print("curDist out is " + str(curDist))
    u.debug_print("During the last "+str(green_light_interval)+" seconds, "+str(i)+" cars passed")


