#! /usr/bin/env python3
"""
Bostin Technology  (see www.BostinTechnology.com)

For use with the CognIoT Sensors and uses the Android Application to read values

Command Line Options
    - Start Capturing Readings (default action)     -s --Start
    - Display Calibration                           -d --DisplayCal
    - Set Calibration                               -e --SetCal
    - Display Operational Parameters                -o --DisplayPara
    - Set Operational Parameters                    -a --SetPara
    - Reset                                         -t --Reset
    - Add New Sensor                                -n --NewSensor
    - Read Device ID                                -d --DeviceID
    - Read Sensor ID                                -o --SensorID

"""

from CognIot import DataAccessor
from CognIot import iCOGUtils
from CognIot import iCOGSensorComms
from datetime import datetime
import time
import argparse

# TODO: Remove these to use from other location
sensor_acroynm = "PirFlx"
sensor_description = "RFID Tag Reader"


def GetSerialNumber():
    """
    Get the System Serial number to be used as the Device ID
    returns the Serial Number or '0000000000000000'
    """
    try:
        f = open('/proc/cpuinfo')
        for line in f:
            if line[0:6] == "Serial":
                cpuserial = line[10:26]
        f.close
    except:
        cpuserial = '0000000000000000'
    print ("CPU Serial Number : %s" % cpuserial)    #Added for Debug Purposes
    return int(cpuserial, 16)


def GenerateTimeStamp():
    """
    Generate a timestamp in the correct format
    dd-mm-yyyy hh:mm:ss.sss
    datetime returns a object so it needs to be converted to a string and then redeuced to 23 characters to meet format
    """
    now = str(datetime.now())
    #print ('Timestamp: %s' % now[:23]) #Debug
    return now[:23]

def SetandGetArguments():
    """
    Define the arguments available for the program and return any arguments set.

    """
    parser = argparse.ArgumentParser(description="Capture and send data for CognIoT sensors")
    parser.add_argument("-S", "--Start",
                    help="Start capturing data from the configured sensors and send them to the database")
    parser.add_argument("-t", "--Reset", 
                    help="Reset to the default values")
    parser.add_argument("-n", "--NewSensor", 
                    help="Add a new Sensor to this Raspberry Pi")
    parser.add_argument("-d", "--DeviceID", 
                    help="Display the Device ID for this Raspberry Pi")
    parser.add_argument("-o", "--SensorID", 
                    help="Display the Sensor IDs being used")
    Cal_group = parser.add_mutually_exclusive_group()
    Cal_group.add_argument("-d", "--DisplayCal", 
                    help="Display the Calibration Data for the sensors")
    Cal_group.add_argument("-e", "--SetCal", 
                    help="Set new Calibration Data for the sensors")
    Para_group = parser.add_mutually_exclusive_group()
    Para_group.add_argument("-o", "--DisplayPara", 
                    help="Display the Operational parameters, e.g. Read Frequency")
    Para_group.add_argument("-a", "--SetPara", 
                    help="Set the Operational parameters, e.g. Read Frequency")

    return parser.parse_args()

def main():
    """
    This routine is the main called routine and therefore determines what action to take based on the arguments given.
    
    """
    args = SetandGetArguments()
    
    # First print a 'splash screen'
    device_id = GetSerialNumber()
    print("Bostin Technology\nRFID Reader")
    print("\nDevice ID: %s" % device_id)
    print("\nTo Exit, CTRL-c\n\n")

    if args.Start:
        #TODO: Move to a separate subroutine
        
        # Default Action
        dbconn = DataAccessor.DynamodbConnection()
        
        #TODO: Read the EEPROM and process the data

        #TODO: Setup the sensors 
        sensor = iCOGSensorComms.SetupHardware( add some parameters in here)

        while True:
            # Read the data
            data_read = iCOGSensorComms.ReadData( add some parameters in here)
            
            if tag_num[0]:
                DataAccessor.WriteValues(dbconn, tag_num[1], GenerateTimeStamp(), device_id, "0001", sensor_acroynm, sensor_description)
    """
    
# Only call the Start routine if the module is being called directly, else it is handled by the calling program
if __name__ == "__main__":
    main()




