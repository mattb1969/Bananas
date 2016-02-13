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

"""
Progress So far


"""


#from . import DataAccessor
#from . import iCOGUtils
#from . import iCOGSensorComms

import DataAccessor
import iCOGUtils
import iCOGSensorComms

from datetime import datetime

import time
import argparse

DATAFILE_NAME = "datafile.txt"
DATAFILE_LOCATION = "CognIoT"


################################################################################
#
# iCOG Class for each sensor being used.
#
################################################################################
class iCOG():
    """
    This class needs to hold everything associated with the sensor
    
    self.datafile contains the information read from the external file.
    """

    def __init__(self):
        #TODO: Read the EEPROM and process the data - could this be set globals function?
        #       Check for a tuple first - if UUID matches, use the data
        #       Create a iCOG class holding the sensor data
        #       turple the data for future use
        """
        INitialises the values and checkes if they have been previously saved as a tuple
        """
        #TODO: Not yet implemented
        #readfrequency is the time between reading of values
        self.readfrequency = 30
        return
    
    def ReturnUUID(self):
        return self.uuid
    
    def ReturnBusType(self):
        return self.bustype
    
    def ReturnBusNumber(self):
        return self.busnumber
        
    def ReturnSensorAddress(self):
        return self.sensoraddress
        
    def ReturnSensor(self):
        return self.sensor
    
    def ReturnManufacturer(self):
        return self.manufacturer
    
    def ReturnReadFrequency(self):
        return self.readfrequency

    def GetSensor(self, sensor_id):
        """
        Interface with the EEPROM and get the sensor details
        Returns
            uuid, bustype, busnumber, sensoraddress, sensor, manufacturer, status
        How will this work for multiple sensors?
        """
        status, reply = iCOGUtils.GetSensor(sensor_id)
        if status:
            self.uuid = reply[0]
            self.bustype = reply[1]
            self.busnumber= reply[2]
            self.sensoraddress = reply[3]
            self.sensor = reply[4]
            self.manufacturer = reply[5]
        else:
            #TODO: Implement something here
            print ("unable to read EEPROM")
            sys.exit()
        
        return 
        
    def SetAcroymnData(self):
        """
        This must be run after GetSensors
        Sets the additional information about the sensor, based on the data file
        Loads the datafile into a 
            - Sensor Acroynm (self.sensoracroynm)
            - Sensor Description (seslf.sensordescription)
            - Read Frequency (self.readfrequency)
        
        #TODO: This should only be run if the customer hasn't set values first.
        """
        #TODO: Validate the error checking around this
        self.datafile = []
        try:
            data = open(DATAFILE_LOCATION + '/' + DATAFILE_NAME, mode='rt')
            lines = data.readlines()
            data.close()
        except:
            print("Failed to Open datafile, please contact support")
            sys.exit()
            
        for f in lines:
            # Read a line of data in and strip any unwanted \n type characters
            dataline = f.strip()
            # split the data by a comma into a list.
            row_data = dataline.split(",")
            self.datafile.append(row_data)
        
        #Now loop through the data string and extract the acroynm and description
        # Uses the self.sensor & self.manufacturer
        for element in self.datafile:
            if element[3] == self.sensor and element[4] == self.manufacturer:
                self.sensoracroynm = element[0]
                self.sensordescription = element[1]

        #TODO: Add something if it is not found!
        
        return

    def SetupSensor(self):
        """
        Calls the hardware routine to initiate comms.
        
        uuid, bustype, busnumber, sensoraddress
        """
        try:
            self.setuphardware = iCOGSensorComms.SetupHardware(self.uuid, self.bustype, self.busnumber, self.sensoraddress)
        except:
            print("Unable to set up comms")
            sys.exit()
            
        return self.setuphardware
       
                
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



################################################################################
# 
# The following functions are the client interaction functions
#
################################################################################

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

def Start():
    """
    Perform the reading of and sending data to the AWS database
    This is the default action if no arguments are passed to the system.
    """

    # setup the connection to the AWS database
    dbconn = DataAccessor.DynamodbConnection()

    # Find out how many sensors are connected
    status, sensor_count = iCOGUtils.GetSensorCount()
    if status == False:
        print("No sensors connected to the Rapsberry Pi")
        sys.exit()

    # for each sensor connected, initialise communications     
    sensor_count = 0
    qty_sensors = iCOGUtils.GetSensorCount()
    if qty_sensors < 1:
        print("No sensors detected")
        sys.exit()
        
    while sensor_count < qty_Sensors:
        #Setup the sensors for each class instance
        
        # for the returned sensor, set all the data
        sensor(sensor_count) = iCOG.GetSensor(sensor_count)
        sensor(sensor_count).SetAcroymnData()
        sensor(sensor_count).SetupSensor()
        
        sensor_count = sensor_count + 1

    # For each sensor, read the values and write them to the AWS database
    # needs to use the read frequency to limit the number of reads.
    
    """
    This next bit would probably benefit from being in threads, using threading
    
    Needs a new class for threading, in the class
        __init__
            - pass in the values it needs
        run
            - check timer
            - read the value
            - post it to AWS
        
    Then in the main bit, start the threads, with each thread being started from within a loop.
    
    
    """
    starttime = time.time()
    while True:
        # Read the data
        for one in sensor:
            #TODO: Set this within a timed loop so it doesn't read data continually for most sensors

            
            #data_read = one.ReadData( add some parameters in here)
            
            # BUG: This line doesn't contain the correct variables
            if tag_num[0]:
                DataAccessor.WriteValues(dbconn, tag_num[1], GenerateTimeStamp(), device_id, "0001", sensor_acroynm, sensor_description)

        #TODO: Consider a method of exiting the loop without using CTRL-C

        
    return

def Reset():
    """
    Reset the program back to using the default values
    Clear any cached sensor data
    
    """
    print ("Not yet Implemented")
    return

def NewSensor():
    """
    Perform the necessary actions to add a new sensor to the system
    """
    print ("Not yet Implemented")
    return

def DisplayDeviceID():
    """
    Display the Device ID to the user
    """
    print ("Not yet Implemented")
    return

def DisplaySensorID():
    """
    Perform the necessary actions to display the Sensor ID being used
    """
    print ("Not yet Implemented")
    return
    
def DisplayCal():
    """
    Perform the necessary actions to display the Calibration data being used
    
    """
    print ("Not yet Implemented")
    return
    
def SetCal():
    """
    Perform the necessary actions to set the Calibration data being used
    
    """
    print ("Not yet Implemented")
    return
    
def DisplayParameters():
    """
    Perform the necessary actions to display the parameter data being used
    
    """
    print ("Not yet Implemented")
    return
    
def SetParameters():
    """
    Perform the necessary actions to allow the clinet to set the parameter data being used
    
    Parameters to be captured
    - Sensor Acroynm
    - Sensor Description
    - Read Frequency
    """
    print ("Not yet Implemented")
    return
 
 
 
################################################################################
# 
# The following function is main - the entry point
#
################################################################################

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
    
    #TODO: print out the values being used, especially if they are the defaults.
    
    #TODO: sort out the global variables, including how many sensors are connected.
    #TODO: prpbably needs something to bomb out if there is a failure
    SetGlobals()

    if args.Start:
        Start()              #TODO: Complete routine
    elif args.Reset: 
        Reset()              #TODO: Not started
    elif args.NewSensor:
        NewSensor()          #TODO: Not started
    elif args.DeviceID:
        DisplayDeviceID()    #TODO: Not started
    elif args.SensorID:
        DisplaySensorID()    #TODO: Not started
    elif args.DisplayCal:
        DisplayCal()         #TODO: Not started
    elif args.SetCal:
        SelCal()             #TODO: Not started
    elif args.DisplayPara:
        DisplayParameters()  #TODO: Not started
    elif args.SetPara:
        SetParameters()      #TODO: Not started
    else:
        Start()

    
        

    
# Only call the Start routine if the module is being called directly, else it is handled by the calling program
if __name__ == "__main__":
    main()




