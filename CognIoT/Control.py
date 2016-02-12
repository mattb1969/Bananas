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
- Currently trying to figure out how to get the data out of the datafile and into a list so I can parse it
  to find the data I want. 
  Once I've got that, I can set the rest of the variables for the sensor connected.
- Absolutely no testing completed at all

- trying to get the test module working so I can have some validation on the code written.
"""


from . import DataAccessor
from . import iCOGUtils
from . import iCOGSensorComms

from datetime import datetime

import time
import argparse




################################################################################
#
# iCOG Class for each sensor being used.
#
################################################################################
class iCOG():
    """
    This class needs to hold everything associated with the sensor
    
    """

    def __init__(self):
        
        return
        
    def SetAcroymnData(self):
        """
        Sets the additional information about the sensor, based on the data file
        Loads the datafile into a 
            - Sensor Acroynm
            - Sensor Description
            - Read Frequency
        """
        #TODO: Need to add lots of error checking around this
        self.table = ""
        with open('CognIoT/datafile.txt', mode='rt') as f:
            # Read a line of data in and strip any unwanted \n type characters
            data = f.readline.strip()
            # split the data by a comma into a list.
            row_data = data.split(",")
            #TODO: May want to consider being cleverer about this and make an outer list and an inner list
            self.table = self.table + row_data
        f.close()
        
        #Now loop through the data string and extract the acroynm and description
        
        #TODO: loop through and find the data
        return self.table

    def GetSensors(self):
        """
        Interface with the EEPROM and get the sensor details
        Returns
            uuid, bustype, busnumber, sensoraddress, sensor, manufacturer, status
        """
        status, reply = iCOGUtils.GetSensors()
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
        
    def SetupSensor(self):
        """
        Calls the hardware routine to initiate comms.
        
        uuid, bustype, busnumber, sensoraddress
        """
        self.setuphardware = iCOGSensorComms.SetupHardware(self.uuid, self.bustype, self.busnumber, self.sensoraddress)

        #TODO: verify the response to check the sensor has initialised correctly.
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

def SetGlobals():
    """
    Set all the global variables being used by the project.
    Can be passed any number of variables and needs to assign accordingly
    
    TODO: Have these pickled after they have been updated and loaded on start
    
    All global variables are lists, entry 0 being the first sensor connected to the Pi.
    
    """
    
    global g_sensor_acroynm
    g_sensor_acroynm = ["PirFlx"]
    global g_sensor_description
    g_sensor_description = ["RFID Tag Reader"]
    # read frequency is stored in seconds
    global g_read_frequency
    g_read_frequency = [1]

    global g_qty_sensors
    g_qty_sensors = iCOGUtils.GetSensorCount()
    #TODO: Add check that if no sensors connected, no further action


        #TODO: Read the EEPROM and process the data - could this be set globals function?
        #       Check for a tuple first - if UUID matches, use the data
        #       Create a iCOG class holding the sensor data
        #       turple the data for future use
    
    #If called from SetParamters, needs to use the new values given

    #TODO: Needs to use the set parameters values also
    return

def GetSensors_OLD():
    """
    Read the Sensor data from the EEPROM and return the values
    GetSensors returns:
    - UUID
    - bustype
    - busnumber
    - sensor address
    - sensor type
    - sensor manufacturer
    
    
    """
    
    # read the status and sensor data from the iCOGUtils function
    answer, sensors = iCOGUtils.GetSensors()

    if answer:
        # postive response means successful read
        # set the global data associated to the sensor read
        return sensors
    else:
        # failed
        time.sleep(0.01)
    return        
    

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


    # for each sensor connected, initialise communications
    sensor_count = 0
    while sensor_count < g_qty_sensors:
        #Setup the sensors for each class instance
        #TODO:  parameters required: uuid, bustype, busnumber, sensoraddress
        
        #BUG: This line is wrong, as it needs to go via the class!!!
        #sensor(sensor_count) = iCOG.SetupSensor( add some parameters in here)
        
        sensor_count = sensor_count + 1

    # For each sensor, read the values and write them to the AWS database
    # needs to use the read frequency to limit the number of reads.
    while True:
        # Read the data
        for one in sensor:
            #TODO: Set this within a timed loop so it doesn't read data continually for most sensors
            #       will need a default value to use
            
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




