#! /usr/bin/env python3
"""
Sensor Class.

Each sensor is an instance of the class

"""

class iCOG():

    def __init__(self):
        
        return
        
    def GetSensors(self):
        """
        Read the Sensor data from the EEPROM and return the values
        GetDevices returns:
        - bustype
        - busnumber
        - sensor address
        - UUID
        - sensor type
        - sensor manufacturer
        """
        
        # read the status and sensor data from the iCOGUtils function
        answer, sensors = iCOGUtils.GetSensors()

        if answer:
            # postive response means successful read
            # set the global data associated to the sensor read
            return sensors
        else
            # failed
            
        return
