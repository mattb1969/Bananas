#! /usr/bin/env python3
"""

This is a stub program for the purposes of testing the main program

"""
import logging



#Bus types
I2C = "I2C"
SPI = "SPI"
SERIAL = "Serial"


def GetSensor(sensor_id):
    """
    The real routines reads the EERPROM and returns various values from it
    This just returns a positive response and some values as a dictionary if it is the first sensor
    else it returns False and an empty set
    
    UUID, bustype, busnumber, sensoraddress, sensor, manufacturer
    """
    log = logging.getLogger(__name__)
    print("Sensor ID Requested %s" % sensor_id)
    log.info("Sensor ID")
    
    if sensor_id == 0:
        bustype = I2C
        busnumber = 1
        sensoraddress = "Ox50"
        uuid= 0x12345678
        sensor = 12
        manufacturer = 1
        status = True
    if sensor_id == 1:
        bustype = I2C
        busnumber = 1
        sensoraddress = "Ox51"
        uuid= 0x00000001
        sensor = 12
        manufacturer = 1
        status = True
    if sensor_id == 2:
        bustype = I2C
        busnumber = 1
        sensoraddress = "Ox52"
        uuid= 0x00000002
        sensor = 12
        manufacturer = 1
        status = True
    else:
        bustype = ""
        busnumber = 0
        sensoraddress = ""
        uuid= 0
        sensor = 0
        manufacturer = 0
        status= False
    
    return status, [uuid, bustype, busnumber, sensoraddress, sensor, manufacturer]

def GetEEPROMData(uuid, bustype, busnumber, sensoraddress,page):
    """
    The real routine reads a page of data from the EEPROM
    This just returns some values as a dictionary
    
    Will return 16 bytes of data
    """
    
    print("To Be Implemented")
    status = True
    return status
    
def SetEEPROMData(uuid, bustype, busnumber, sensoraddress, page, data):
    """
    The real routine writes a page of data from the EEPROM
    This just returns some values as a dictionary
    
    Will return a status only
    """
    
    print("To Be Implemented")
    status = True
    return status
    
def VerifyChecksum():
    """
    The real routine reads and checks the values of data against the checksum
    Will return True / False
    
    This routine always passes!
    """
    
    return True

def SetChecksum():
    """
    The real routine calculates a new checksum and writes it to the checksum field
    Will return True if the calculation and write are successful / False if not
    
    This routine always passes!
    """
    
    return True

def GetSensorCount():
    """
    the real routine determines how manyu sensors are connected somehow
    This just returns a status and fixed value
    """
    
    return True, 3
