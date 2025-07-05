#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018
@author: David Fasani, ICAM
'''

from __future__ import print_function
from dronekit import  VehicleMode, LocationGlobalRelative
from test5 import init_vehicle
import urllib.request
import time


"""
    Arms vehicle and fly to aTargetAltitude.
"""
def arm_and_takeoff(aTargetAltitude):
    

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

vehicle = init_vehicle(3.97002, 9.7919)

arm_and_takeoff(10)
action = "Goto"

#while the vehicule is in GUIDED mode(vehicle.mode == "GUIDED")
while action == "Goto" :
    
    url = "https://op-dev.icam.fr/~icam/Group8.txt"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    lat,lon,action = response.read().decode('utf-8').split()
    print("lat: ", lat)
    print("lon: ", lon)
    print("action: ",action)
    print("")
    
    lat = float(lat)
    lon = float(lon)
    
    vehicle.simple_goto(LocationGlobalRelative(lat,lon,20), airspeed=100)
    
    time.sleep(1)



# Close vehicle object before exiting script
print("Closing vehicle object...")
vehicle.close()


print("Goodbye !")
