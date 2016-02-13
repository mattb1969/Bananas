#! /usr/bin/env python3
"""
Bostin Technology  (see www.BostinTechnology.com)

Test module to validate the code written as part of the iCOGSensors

Further test scripts to add
- AWS Database connections
- all arguments being passed in
"""




import os
import sys

sys.path.append("/home/pi/Bananas/CognIoT")
print ("System Path: %s" % sys.path)
#from .Control import Control
#from .Control 
import Control

def TestFileLoading():
    """
    Routine to test the loading of the file
    
    #TODO: Make it fail by not finding the file
    #TODO: Make it fail by having corrupt data
    """
    acr = Control.iCOG()
    oput = acr.SetAcroymnData()
    
    #TODO: Validate the response from the function
    print ("Response from function %s" %oput)
    return

if __name__ == "__main__":
    """
    
    Entry Point for running test scripts
    
    """
    
    TestFileLoading()
    




