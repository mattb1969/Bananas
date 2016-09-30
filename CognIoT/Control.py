#! /usr/bin/env python3
"""
Bostin Technology  (see www.BostinTechnology.com)

For use with the CognIoT Sensors and uses the Android Application to read values

Command Line Options
    - Start Capturing Readings (default action)     -s --Start
    - Display Calibration                           -c --DisplayCal
    - Set Calibration                               -e --SetCal
    - Display Operational Parameters                -o --DisplayPara
    - Set Operational Parameters                    -a --SetPara
    - Reset                                         -t --Reset
    - Add New Sensor                                -n --NewSensor
    - Read Device ID                                -d --DeviceID
    - Read Sensor ID                                -i --SensorID
    - Set Logging Level                             -l --Logging

"""

"""
Progress So far
Written the first cut for the capturing of readings, ready for some testing
- ideally need to write some unit tests to do all this stuff, rather than rely on manual testing.


BUG - logging is creating the file, but it is not logging from the sub modules.
    Could be related to the modules being loaded before logging is set up
    see http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
BUG - When it is trying to access the datafile, it is using relative paths and therefore
    has to be run from only the parent directory
BUG - After loading the datafile, it is unable to find a match in the datafile
BUG - Print statements are not working, in sub files - Eg. IN DataAccessor it should print the values 
    it is trying to write to the database, it doesn't.
BUG - In the threading it is writing values, but no longer exiting the loops


PLus other BUGs in the file below!!!

TODO: Modify the software to always put the log file in a fixed 'standard' directory and to make it time / size bound
TODO: Modify the threading to use the thread timer function rather than doing it myself.

"""


import DataAccessor
import iCOGUtils
import iCOGSensorComms
import threading

from datetime import datetime

import time
import argparse
import sys
import logging


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
        Initialises the values and checkes if they have been previously saved as a tuple
        """
        #TODO: Not yet implemented
        #readfrequency is the time between reading of values

#BUG - This should be set higher, but is changed for testing
        self.readfrequency = 3
        log.debug("iCOG initialised, read frequency set to %s" % self.readfrequency)
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

    def GetSensorDataFromEEPROM(self, sensor_id):
        """
        Interface with the EEPROM and get the sensor details
        Sets
            uuid, bustype, busnumber, sensoraddress, sensor, manufacturer, status
        for each sensor as a unique class object
        """
        status, reply = iCOGUtils.GetSensor(sensor_id)
        log.debug("Got sensor status and data from iCOGUtils: %s : %s" % (status, reply))
        if status:
            self.uuid = reply[0]
            self.bustype = reply[1]
            self.busnumber= reply[2]
            self.sensoraddress = reply[3]
            self.sensor = reply[4]
            self.manufacturer = reply[5]
            log.info("Loaded Sensor information")
        else:
            #TODO: Implement something here
            log.critical("Unable to Read EEPROM, program halted")
            #print ("unable to read EEPROM") removed as now log statement
            sys.exit()
        
        return 
        
    def SetAcroymnData(self):
        """
        This must be run after GetSensorDataFromEEPROM
        Sets the additional information about the sensor, based on the data file
        Loads the datafile into a 
            - Sensor Acroynm (self.sensoracroynm)
            - Sensor Description (seslf.sensordescription)
            - Read Frequency (self.readfrequency)
        
        #TODO: This should only be run if the customer hasn't set values first.
        #TODO: Reading fo the datafile should only be done once and not for each sensor
        """
        #TODO: Validate the error checking around this
        self.datafile = []
        log.info("Reading the datafile for sensor information")
        try:
            log.debug("DataFile in location:%s" % DATAFILE_LOCATION + '/' + DATAFILE_NAME)
            data = open(DATAFILE_LOCATION + '/' + DATAFILE_NAME, mode='rt')
            lines = data.readlines()
            data.close()
            log.debug("datafile loaded %s" % lines)
        except:
            log.critical("Failed to Open datafile, please contact support", exc_info=True)
            sys.exit()

        log.info("Decoding the datafile, line by line")
        for f in lines:
            # Read a line of data in and strip any unwanted \n type characters
            dataline = f.strip()
            # split the data by a comma into a list.
            row_data = dataline.split(",")
            self.datafile.append(row_data)
            log.debug("Row of extracted data %s" % row_data)
            
        #Now loop through the data string and extract the acroynm and description
        log.info("Loop through datafile and set sensor information")
        # Uses the self.sensor & self.manufacturer
        for element in self.datafile:
            if element[3] == self.sensor and element[4] == self.manufacturer:
                log.debug("Match found for Sensor and Description")
                self.sensoracroynm = element[0]
                self.sensordescription = element[1]
                
            else:
                log.warning("No match found for Sensor and Description, using defaults")
                self.sensoracroynm = "UNK"
                self.sensordescription = "Sensor Description Unknown, contact support"
                
        log.debug("Sensor: %s and Manufacturer:%s match found, loading acroynm:%s and desc:%s" 
            %(self.sensor, self.manufacturer, self.sensoracroynm, self.sensordescription))        
        
        return

    def SetupSensor(self):
        """
        Calls the hardware routine to initiate comms.
        
        uuid, bustype, busnumber, sensoraddress
        """
        log.info("Setting up hardware")
        try:
            self.setuphardware = iCOGSensorComms.SetupHardware(self.uuid, self.bustype, self.busnumber, self.sensoraddress)
            log.debug("Setup comms with the sensor: %s" % self.setuphardware)
        except:
            logging.critical("Unable to set up comms, contact support")
            sys.exit()
            
        return self.setuphardware

################################################################################
#
# Threading Class to manage and control the reading threads.
#
################################################################################
class ReadingThread(threading.Thread):
    """
    To perform the operations for the reading of the sensors within threads.
    
        Needs a new class for threading, in the class
        __init__
            - pass in the values it needs
        run
            - check timer
            - read the value
            - post it to AWS
    """
    
    def __init__(self, sensor, dbconnection):
        threading.Thread.__init__(self)
        self.log = logging.getLogger(__name__)
        self.sensor = sensor
        # self.event contains the 'event' received to run / stop the threads
        self.event = threading.Event()
        self.threadname = threading.currentThread().getName()
        self.log.info("Thread:%s for Sensor:%s initialised" % (self.threadname, self.sensor.sensoracroynm))
        self.conn = dbconnection
        return
    
    def run(self):
        self.log.info("Thread:%s for Sensor:%s running" % (self.threadname, self.sensor.sensoracroynm))
        
        self.starttime = time.time()
        # If exitFlag is True, time to stop!
        self.log.debug("Thread Sensor Read Frequency:%f" % self.sensor.readfrequency)
        self.log.info("Thread Event setting:%s" % self.event.is_set())
        while not self.event.is_set():
            #Is it time to read the sensor?
            if (time.time()- self.starttime) > self.sensor.readfrequency:
                self.log.debug("Thread Time to read values for thread:%s" % self.threadname)
                # Read the data (uuid, bustype, busnumber, deviceaddress)
                info = iCOGSensorComms.ReadData(self.sensor.uuid, self.sensor.bustype, self.sensor.busnumber, self.sensor.sensoraddress)
                self.log.debug("Thread %s: Read data from Sensor: %s" %( self.threadname, info))

                #Write the data from the sensor to the database
                DataAccessor.WriteValues(self.conn, info, GenerateTimeStamp(), self.sensor.uuid, self.sensor.sensor, self.sensor.sensoracroynm, self.sensor.sensordescription)
                self.log.debug("Thread %s has written data to AWS" % self.threadname)

                # Reset the timer
                self.starttime = time.time()
            #self.log.debug("Time elapsed during loop check:%f" %(starttime - time.time()))
        self.log.info("Thread:%s for Sensor:%s finishing" % (self.threadname, self.sensor.sensoracroynm))
        return
    
    def stop(self):
        # When called, this sets the running flag to false to stop all instances of the class.
        
        self.log.info("Stop method called")
        self.event.set()
        return
        





################################################################################
#
# Main section
#
################################################################################

                
def GetSerialNumber():
    """
    Get the System Serial number to be used as the Device ID
    returns the Serial Number or '0000000000000000'
    """
    try:
        log.debug("Opening proc/cpuinfo for CPU serial Number")
        f = open('/proc/cpuinfo')
        for line in f:
            if line[0:6] == "Serial":
                cpuserial = line[10:26]
        f.close
    except:
        cpuserial = '0000000000000000'
        log.error("Failed to open proc / cpuinfo, set to default")

    log.info("CPU Serial Number : %s" % cpuserial)
    return int(cpuserial, 16)

def GenerateTimeStamp():
    """
    Generate a timestamp in the correct format
    dd-mm-yyyy hh:mm:ss.sss
    datetime returns a object so it needs to be converted to a string and then redeuced to 23 characters to meet format
    """
    now = str(datetime.now())
    log.debug("Generated a timestamp %s" % now[:23])
    return now[:23]

def SetupLogging():
    """
    Setup the logging defaults
    Using the logger function to span multiple files.
    """
    print("Current logging level is \n\n   DEBUG!!!!\n\n")
    
    # Create a logger with the name of the function
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)      #Set to the highest level, actual logging level set for each handler.
    
    # Create a file handler to write log info to the file
    fh = logging.FileHandler('CognIoT.log', mode='w')
    fh.setLevel(logging.DEBUG)      #This is the one that needs to be driven by user input
    
    # Create a console handler with a higher log level to output logging info of ERROR or above to the screen (default output)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Create a formatter to make the actual logging better readable
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    #BUG: This is loading the wrong values into the log file
    log.info("File Logging Started, current level is %s" % log.getEffectiveLevel)
    log.info("Screen Logging Started, current level is %s" % log.getEffectiveLevel)
    
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
    log.info("Setting and Getting Parser arguments")
    parser = argparse.ArgumentParser(description="Capture and send data for CognIoT sensors")
    parser.add_argument("-S", "--Start",
                    help="Start capturing data from the configured sensors and send them to the database")
    parser.add_argument("-t", "--Reset", 
                    help="Reset to the default values")
    parser.add_argument("-n", "--NewSensor", 
                    help="Add a new Sensor to this Raspberry Pi")
    parser.add_argument("-d", "--DeviceID", 
                    help="Display the Device ID for this Raspberry Pi")
    parser.add_argument("-i", "--SensorID", 
                    help="Display the Sensor IDs being used")
    parser.add_argument("-l", "--Logging", 
                    help="Set the logging level to be used (Default is OFF)")
    Cal_group = parser.add_mutually_exclusive_group()
    Cal_group.add_argument("-c", "--DisplayCal", 
                    help="Display the Calibration Data for the sensors")
    Cal_group.add_argument("-e", "--SetCal", 
                    help="Set new Calibration Data for the sensors")
    Para_group = parser.add_mutually_exclusive_group()
    Para_group.add_argument("-o", "--DisplayPara", 
                    help="Display the Operational parameters, e.g. Read Frequency")
    Para_group.add_argument("-a", "--SetPara", 
                    help="Set the Operational parameters, e.g. Read Frequency")

    log.debug("Parser values captured: %s" % parser.parse_args())
    return parser.parse_args()

def Start():
    """
    Perform the reading of and sending data to the AWS database
    This is the default action if no arguments are passed to the system.
    """

    # setup the connection to the AWS database
    dbconn = DataAccessor.DynamodbConnection()
    log.info("Connected to AWS database")
    log.debug("Database connection:%s" % dbconn)

    # Find out how many sensors are connected
    status, qty_sensors = iCOGUtils.GetSensorCount()
    log.info("Status: %s and Number of Sensors Connected:%s" % (status, qty_sensors))
    if status == False:
        log.critical("No sensors connected to the Rapsberry Pi, program halted")
        print("No sensors connected to the Rapsberry Pi, program halted")
        sys.exit()
    
    sensor = []
    log.debug("Qty Sensors: %d" % qty_sensors)
    for c in range(0, qty_sensors):
        #Setup the sensors for each class instance
        sensor.append(iCOG())

    log.debug("List of Sensors: %s" % sensor)
    # for each sensor connected, initialise communications     
    sensor_count = 0
    for sens in sensor:
        sens.GetSensorDataFromEEPROM(sensor_count)
        sens.SetAcroymnData()
        sens.SetupSensor()
        sensor_count = sensor_count + 1        

    log.info("Starting Threading for reading of values")
    # For each sensor, read the values and write them to the AWS database
    # needs to use the read frequency to limit the number of reads.
    
    threadID = 1

    threads = []
    # Create the new threads, using the run function within ReadingThread
    for tsensor in sensor:
        # Trying to pass in the individual sensor into the thread, no idea if it will work!!
        thread = ReadingThread(tsensor,dbconn)
        thread.start()
        threads.append(thread)
        threadID = threadID + 1
        log.debug("Added Thread %s as ID: %d" % (tsensor, threadID))

    log.info("All the Threads are Running")
    # Wait for the user to exit via the keyboard.
    key = input("\nPress Enter to Exit\n")
        
    
    # Wait for the threads to complete
    for t in threads:
        log.debug("Waiting for the thread:%s to complete" %t)
        t.event.set()

        t.join()
        
    log.debug("Exiting Main Thread")
    
    
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

def SetLogging():
    """
    Perform the necessary actions to achange the logging level being used

    The default logging level is zero
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
    
    SetupLogging()
    
    args = SetandGetArguments()
    
    # First print a 'splash screen'
    device_id = GetSerialNumber()
    print("Bostin Technology\nRFID Reader")
    print("\nDevice ID: %s" % device_id)
    print("\nTo Exit, CTRL-c\n\n")
    
    #TODO: print out the values being used, especially if they are the defaults.
    
    #TODO: probably needs something to bomb out if there is a failure

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
    elif args.Logging:
        SetLogging()         #TODO: Not started
    else:
        Start()

    
        

    
# Only call the Start routine if the module is being called directly, else it is handled by the calling program
if __name__ == "__main__":

    main()




