from distutils.core import setup
setup(name='CypressCapsense_I2C',
      version='0.1.0',
      description='Python module for communicating with Cypress Capsense CY8C201xx capacitive touch sensors over I2C',
      author='Rosangela Canino-Koning',
      author_email='cypresscapsensei2c@voidptr.net',
      url='https://github.com/voidptr/CypressCapsense/',
      license='GPL',
      py_modules=['CypressCapsense_I2C'],
      requires=['smbus'],
      long_description="""
Python Library for Cypress Capsense C8YC201xx over I2C
======================================================

GitHub: https://github.com/voidptr/CypressCapsense/tree/master/BeagleBone

This library requires the SMBus Linux i2c libray. It has been tested on the 
BeagleBone, but it should work on any linux system that supports I2C.

For example::

    import CypressCapsense_I2C

    ####### INITIAL SETUP - Only Do Once Per Device
    # sensorInit = CypressCapsense_I2C.CypressCapsense_I2C(0x00, debug=True)
    # sensorInit.setupDevice()
    # sensorInit.changeDeviceAddress(0x5D) # or whatever address you want
    ########################################################################


    ## this device has already been set up to use 0x5D as its address
    sensor = CypressCapsense_I2C.CypressCapsense_I2C(0x5D, debug=False)

    while(True):
        print "0x%02X" % sensor.fetchTouchStatus()


External Documentation
----------------------

Cypress Capsense CY8C201xx
^^^^^^^^^^^^^^^^^^^^^^^^^^
http://www.cypress.com/?id=1377

CY8C201xx Register Reference Guide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
http://www.cypress.com/?rID=14664
http://www.cypress.com/?docID=41921

CY8C201xx Datasheet
^^^^^^^^^^^^^^^^^^^
http://www.cypress.com/?rID=3912
http://www.cypress.com/?docID=50758

Idiosyncracies
--------------

I2C Address
^^^^^^^^^^^

The CypressCapsense chip should be initialized with an address. Per
http://www.cypress.com/?id=4&rID=29387, the default address is 0x00. If you are 
communicating with multiple Cypress Capsense devices, you must reset the 
default address using the *changeDeviceAddress* function in this library.

To confirm the value of your device's address, you may disconnect all other 
unknown devices except for the Capsense, and then run::

    $ i2cdetect -y -r 1

Setting the address only needs to be done once.

Setting the address works from Arduino devices, and probably from BeagleBone.
PIC-based devices such as the ChipKit cannot be used to re-set the address 
however, because they reserve address 0x00 for some internal purpose.

Sensible Defaults
^^^^^^^^^^^^^^^^^

This library includes a function to set sensible defaults on the Capsense
chip (*setupDevice*). By default, it disables every gpio, turns on every 
touch sensor, and sets the capacitive sensing thresholds to reasonable values.

All that said, these settings may no be sensible FOR YOU. The GPIO and 
CapSense settings may be set via SetupDevice, but to set different sensing 
thresholds, you must apply those settings yourself, using the *write* 
primitive.

To set these values, you must place the device in SETUP_OPERATION_MODE, apply
the setting, then save, and restart::

    sensor.write(CSE_COMMAND_REG, SETUP_OPERATION_MODE);
    sensor.write(CypressCapsense_I2C.CSE_CS_OTH_SET, (CypressCapsense_I2C.CSE_OTH_SET_DISABLE_EXT_CAP | CypressCapsense_I2C.CSE_OTH_SET_SENSOR_RESET | CypressCapsense_I2C.CSE_OTH_SET_CLOCK_IMO))
    sensor.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.STORE_CURRENT_CONFIGURATION_TO_NVM)
    sensor.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.RECONFIGURE_DEVICE)
    sensor.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.NORMAL_OPERATION_MODE)


Device setup only needs to be done once. The settings are stored in 
non-volatile memory across restarts.

Sensing Reset
^^^^^^^^^^^^^

Per the manufacturer, the Capsense chip has mechanisms for adjusting to the 
environment over time to maintain the sensitivity and accuracy of the sensor.

In my board designs, however, I find whatever method they are using to be 
hilariously ineffective. Therefore, it is prudent to reset the board sensors
periodically. This may be done via the *reset* function::

    sensor.reset()


Buffer Reading
^^^^^^^^^^^^^^

For some reason, the Capsense device doesn't like responding to the buffer-
reading capabilities in the SMBus library. The SMBus *read_byte(addr)* 
primitive should do the trick, but it just hangs. So, that means that we can't 
read i2c buffers for the device configration and version number like we can
in the Arduino driver.

Ultimately, this removes some debugging capability on the device, but for the
basic purpose of setting up and reading touch status, this library does the 
trick. YMMV.

Todo
----

Sliders
^^^^^^^

Some Capsense chips have the capability to provide hardware-mediated sliders.
Users of this library are able to set the appropriate settings to use these
capabilities using the *write* primitive, but easy support during SetupDevice
is not yet available. Stay tuned.

PyDoc Output for CypressCapsense_I2C
====================================

Help on module CypressCapsense_I2C::

    NAME
        CypressCapsense_I2C

    FILE
        /home/rosiec/CypressCapsense/BeagleBone/CypressCapsense_I2C.py

    CLASSES
        CypressCapsense_I2C
        
        class CypressCapsense_I2C
         |  Methods defined here:
         |  
         |  __init__(self, address, busnum=-1, debug=False)
         |  
         |  changeDeviceAddress(self, new_address)
         |      Parameters:
         |          new_address - 7 Bit new device address to set
         |          
         |      Return Value:
         |          none
         |      
         |      Errors:
         |          none
         |      
         |      Description:
         |          Sends command to device to unlock the address register, change the address
         |          value, and re-lock the register.
         |  
         |  errMsg(self)
         |  
         |  fetchRawCounts(self, port, sensor)
         |      Parameters:
         |          port - Which port to query (0 or 1)
         |          sensor - Which sensor to query (0-4)
         |      
         |      Return Value:
         |          uint16_t - The raw count of the sensor.
         |      
         |      Errors:
         |          If port > 1, or sensor > 4, return 0
         |      
         |      Description:
         |          Fetches the raw count values from the sensor
         |  
         |  fetchTouchStatus(self)
         |      Parameters:
         |      
         |      Return Value:
         |          uint16_t - The status of the sensors. Each bit being on/off
         |      
         |      Errors:
         |          none
         |      
         |      Description:
         |          Fetches the touch true/false status from the sensors
         |  
         |  read(self, register_address)
         |      Parameters:
         |          register_address - 8 Bit register address designating where to read
         |      
         |      Return Value:
         |          byte
         |      
         |      Errors:
         |          none
         |      
         |      Description:
         |          reads from the Capsense device
         |          to get the data at that location and returns a byte
         |  
         |  readString(self, register_address, size)
         |      Parameters:
         |          register_address - 8 Bit register_address designating where to read
         |          size - number of bytes to be read
         |      
         |      Return Value:
         |          results
         |      
         |      Errors:
         |          none
         |      
         |      Description:
         |          reads consecutive bytes starting
         |          from the given register_address
         |  
         |  reboot(self)
         |      Reboot the board.
         |  
         |  reset(self)
         |      Reset the touch sensors baseline value.
         |  
         |  setupDevice(self, gpio, capsense)
         |      Parameters:
         |          gpio - 16 bits to turn on as GPIO xxxBBBBBxxxBBBBB
         |                 (LSB 8 bits (LSB 5 bits) for GPIO0, MSB 8 bits (LSB 5 bits) GPIO1)
         |          capsense - 16 bits to turn on as Capsense xxxBBBBBxxxBBBBB
         |                     (LSB 8 bits (LSB 5 bits) for GPIO0, MSB 8 bits (LSB 5 bits) GPIO1)
         |      
         |      Return Value:
         |          none
         |      
         |      Errors:
         |          If the pin settings conflict, return false
         |      
         |      Description:
         |          Sets the pins to be used as capsense or GPIO on ports 0 and 1. A pin may not be
         |          both capsense and gpio at the same time.
         |  
         |  write(self, register_address, data)
         |      Parameters:
         |          register_address - 8 Bit register_address designating were to write
         |          data - Data to be written
         |      
         |      Return Value:
         |      
         |      Errors:
         |      
         |      Description:
         |          writes a byte to specified register_address
         |  
         |  writeString(self, register_address, data)
         |      Parameters:
         |          register_address - 8 Bit register_address designating were to write
         |          data - Data to be written
         |      
         |      Return Value:
         |          none
         |      
         |      Errors:
         |          none
         |      
         |      Description:
         |          Writes a string of bytes to
         |          specified register_address. If amount of bytes is above 64 the data
         |          will automaticly be truncated.
         |  
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |  
         |  CSE_COMMAND_REG = 160
         |  
         |  CSE_CS_ENABLE0 = 6
         |  
         |  CSE_CS_ENABLE1 = 7
         |  
         |  CSE_CS_FILTERING = 86
         |  
         |  CSE_CS_FINGER_TH_00 = 97
         |  
         |  CSE_CS_FINGER_TH_01 = 98
         |  
         |  CSE_CS_FINGER_TH_02 = 99
         |  
         |  CSE_CS_FINGER_TH_03 = 100
         |  
         |  CSE_CS_FINGER_TH_04 = 101
         |  
         |  CSE_CS_FINGER_TH_10 = 102
         |  
         |  CSE_CS_FINGER_TH_11 = 103
         |  
         |  CSE_CS_FINGER_TH_12 = 104
         |  
         |  CSE_CS_FINGER_TH_13 = 105
         |  
         |  CSE_CS_FINGER_TH_14 = 106
         |  
         |  CSE_CS_IDAC_00 = 107
         |  
         |  CSE_CS_IDAC_01 = 108
         |  
         |  CSE_CS_IDAC_02 = 109
         |  
         |  CSE_CS_IDAC_03 = 110
         |  
         |  CSE_CS_IDAC_04 = 111
         |  
         |  CSE_CS_IDAC_10 = 112
         |  
         |  CSE_CS_IDAC_11 = 113
         |  
         |  CSE_CS_IDAC_12 = 114
         |  
         |  CSE_CS_IDAC_13 = 115
         |  
         |  CSE_CS_IDAC_14 = 116
         |  
         |  CSE_CS_OTH_SET = 81
         |  
         |  CSE_CS_READ_BUTTON = 129
         |  
         |  CSE_CS_READ_RAWL = 135
         |  
         |  CSE_CS_READ_RAWM = 134
         |  
         |  CSE_CS_READ_STATUS0 = 136
         |  
         |  CSE_CS_READ_STATUS1 = 137
         |  
         |  CSE_CS_SCAN_POS_00 = 87
         |  
         |  CSE_CS_SCAN_POS_01 = 88
         |  
         |  CSE_CS_SCAN_POS_02 = 89
         |  
         |  CSE_CS_SCAN_POS_03 = 90
         |  
         |  CSE_CS_SCAN_POS_04 = 91
         |  
         |  CSE_CS_SCAN_POS_10 = 92
         |  
         |  CSE_CS_SCAN_POS_11 = 93
         |  
         |  CSE_CS_SCAN_POS_12 = 94
         |  
         |  CSE_CS_SCAN_POS_13 = 95
         |  
         |  CSE_CS_SCAN_POS_14 = 96
         |  
         |  CSE_GPIO_ENABLE0 = 8
         |  
         |  CSE_GPIO_ENABLE1 = 9
         |  
         |  CSE_I2C_ADDR_DM = 124
         |  
         |  CSE_I2C_DEV_LOCK = 121
         |  
         |  CSE_OTH_SET_CLOCK_IMO = 0
         |  
         |  CSE_OTH_SET_CLOCK_IMO2 = 32
         |  
         |  CSE_OTH_SET_CLOCK_IMO4 = 64
         |  
         |  CSE_OTH_SET_CLOCK_IMO8 = 96
         |  
         |  CSE_OTH_SET_DISABLE_EXT_CAP = 2
         |  
         |  CSE_OTH_SET_ENABLE_EXT_CAP = 2
         |  
         |  CSE_OTH_SET_NO_SENSOR_RESET = 0
         |  
         |  CSE_OTH_SET_SENSOR_RESET = 8
         |  
         |  CS_FILTERING_TOUCH_BASELINE_RESET = 64
         |  
         |  GET_FIRMWARE_REVISION = 0
         |  
         |  NORMAL_OPERATION_MODE = 7
         |  
         |  READ_DEVICE_CONFIGURATION = 5
         |  
         |  RECONFIGURE_DEVICE = 6
         |  
         |  SETUP_OPERATION_MODE = 8
         |  
         |  STORE_CURRENT_CONFIGURATION_TO_NVM = 1
         |  
         |  lock = [150, 90, 195]
         |  
         |  unlock = [60, 165, 105]



"""
      )
