#! /usr/bin/env python3
"""

This is a stub program for the purposes of testing the main program

"""

#Bus types
I2C = "I2C"
SPI = "SPI"
SERIAL = "Serial"


def GetDevices():
    """
    The real routines reads the EERPROM and returns various values from it
    This just returns a positive response and some values as a dictionary
    
    bustype, busnumber, deviceaddress, UUID, device, manufacturer
    """
    
    bustype = I2C
    busnumber = 1
    deviceaddress = "Ox52"
    UUID = 0x12345678
    device = 12
    manufacturer = 1
    status = True
    
    return status, [bustype, busnumber, deviceaddress, UUID, device, manufacturer]

GetEEPROMData(bustype, busnumber, deviceaddress,page):
    """
    The real routine reads a page of data from the EEPROM
    This just returns some values as a dictionary
    
    Will return 16 bytes of data
    """
    
    print("To Be Implemented")
    status = True
    return status
    
SetEEPROMData(bustype, busnumber, deviceaddress, page, data):
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

