#! /usr/bin/env python3
"""

This is a stub program for the purposes of testing the main program

"""

import logging




def SetupHardware(uuid, bustype, busnumber, sensoraddress):
    """
    
    The real routine sets up the comms for the sensor attached to the PI
    This just returns a positive status and an object representing the sensor
    
    """
    log = logging.getLogger(__name__)
    #TODO: needs to return an istance of iteself
    log.info("Setting Up Hardware")
    
    return True

def ReadData(uuid, bustype, busnumber, deviceaddress):
    """
    
    The real routine sets up the comms for the sensor attached to the PI
    This just returns a positive status and an object representing the sensor
    
    """
    log = logging.getLogger(__name__)
    sensor_data = {"0.01", "35"}
    
    return True, sensor_data
