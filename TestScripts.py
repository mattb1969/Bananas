#! /usr/bin/env python3
"""
Bostin Technology  (see www.BostinTechnology.com)

Test module to validate the code written as part of the iCOGSensors

"""

from CognIoT import Control

def TestFileLoading():
    """
    Routine to test the loading of the file
    
    """
    oput = Control.iCOG.SetAcroymnData()
    
    print ("Response from function %s" %oput)
    return

if __name__ == "__main__":
    """
    
    Entry Point for running test scripts
    
    """
    
    TestFileLoading()
    




