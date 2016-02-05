#! /usr/bin/env python3
"""

This is a stub program for the purposes of testing the main program

"""

def SetupHardware(bustype, busnumber, deviceaddress, UUID):
    """
    
    The real routine sets up the comms for the sensor attached to the PI
    This just returns a positive status and an object representing the sensor
    
    """
    
    return True

def ReadData(bustype, busnumber, deviceaddress, UUID):
    """
    
    The real routine sets up the comms for the sensor attached to the PI
    This just returns a positive status and an object representing the sensor
    
    """
    
    sensor_data = {"0.01", "35"}
    
    return True, sensor_data
