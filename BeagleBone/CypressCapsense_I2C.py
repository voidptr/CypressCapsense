#!/usr/bin/python

import smbus

# ===========================================================================
# CypressCapsense_I2C Class
# Communicates with the Cypress Capsense C8YC20xx Capacitive Touch Module 
# ===========================================================================

# ===========================================================================
# Library based on example Adafruit_I2C, Copyright (c) 2012-2013 Limor Fried, 
#  Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without 
#  modification, are permitted provided that the following conditions are met: 
#  * Redistributions of source code must retain the above copyright notice, 
#  this list of conditions and the following disclaimer. * Redistributions in 
#  binary form must reproduce the above copyright notice, this list of 
#  conditions and the following disclaimer in the documentation and/or other 
#  materials provided with the distribution. * Neither the name of the nor the 
#  names of its contributors may be used to endorse or promote products 
#  derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
#  ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, 
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
#  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ===========================================================================

# ===========================================================================
# Commands based on Cypress Capsense example code, Copyright (c) 2011 Nanwei 
#  Gong & Nan Zhao
# ===========================================================================

# ===========================================================================
# Copyright (c) 2014 Rosangela Canino-Koning. All right reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
# ===========================================================================

class CypressCapsense_I2C :

    # unlock/lock strings
    unlock = [ 0x3C, 0xA5, 0x69 ]
    lock = [ 0x96, 0x5A, 0xC3 ]

    # register addresses
    CSE_CS_ENABLE0 = 0x06
    CSE_CS_ENABLE1 = 0x07

    CSE_GPIO_ENABLE0 = 0x08
    CSE_GPIO_ENABLE1 = 0x09

    CSE_I2C_DEV_LOCK = 0x79
    CSE_I2C_ADDR_DM = 0x7C
    CSE_COMMAND_REG = 0xA0

    CSE_CS_READ_BUTTON = 0x81 # which button shows up in raw counts.

    CSE_CS_READ_RAWM = 0x86 # raw counts
    CSE_CS_READ_RAWL = 0x87

    CSE_CS_FILTERING = 0x56

    CSE_CS_SCAN_POS_00 = 0x57
    CSE_CS_SCAN_POS_01 = 0x58
    CSE_CS_SCAN_POS_02 = 0x59
    CSE_CS_SCAN_POS_03 = 0x5A
    CSE_CS_SCAN_POS_04 = 0x5B
    CSE_CS_SCAN_POS_10 = 0x5C
    CSE_CS_SCAN_POS_11 = 0x5D
    CSE_CS_SCAN_POS_12 = 0x5E
    CSE_CS_SCAN_POS_13 = 0x5F
    CSE_CS_SCAN_POS_14 = 0x60

    CSE_CS_FINGER_TH_00 = 0x61
    CSE_CS_FINGER_TH_01 = 0x62
    CSE_CS_FINGER_TH_02 = 0x63
    CSE_CS_FINGER_TH_03 = 0x64
    CSE_CS_FINGER_TH_04 = 0x65
    CSE_CS_FINGER_TH_10 = 0x66
    CSE_CS_FINGER_TH_11 = 0x67
    CSE_CS_FINGER_TH_12 = 0x68
    CSE_CS_FINGER_TH_13 = 0x69
    CSE_CS_FINGER_TH_14 = 0x6A

    CSE_CS_IDAC_00 = 0x6B
    CSE_CS_IDAC_01 = 0x6C
    CSE_CS_IDAC_02 = 0x6D
    CSE_CS_IDAC_03 = 0x6E
    CSE_CS_IDAC_04 = 0x6F
    CSE_CS_IDAC_10 = 0x70
    CSE_CS_IDAC_11 = 0x71
    CSE_CS_IDAC_12 = 0x72
    CSE_CS_IDAC_13 = 0x73
    CSE_CS_IDAC_14 = 0x74

    CS_SLID_CONFIG = 0x75
    CS_SLID_MULM = 0x77
    CS_SLID_MULL = 0x78

    CSE_CS_OTH_SET = 0x51
    CSE_OTH_SET_DISABLE_EXT_CAP = 0x02 # 0b00000010
    CSE_OTH_SET_ENABLE_EXT_CAP = 0x02  # 0b00000010
    CSE_OTH_SET_NO_SENSOR_RESET = 0x0  # 0b00000000
    CSE_OTH_SET_SENSOR_RESET = 0x8     # 0b00001000
    CSE_OTH_SET_CLOCK_IMO = 0x0        # 0b00000000
    CSE_OTH_SET_CLOCK_IMO2 = 0x20      # 0b00100000
    CSE_OTH_SET_CLOCK_IMO4 = 0x40      # 0b01000000
    CSE_OTH_SET_CLOCK_IMO8 = 0x60      # 0b01100000

    CSE_CS_READ_STATUS0 = 0x88 # on off
    CSE_CS_READ_STATUS1 = 0x89

    # commands
    SETUP_OPERATION_MODE = 0x08
    STORE_CURRENT_CONFIGURATION_TO_NVM = 0x01
    RECONFIGURE_DEVICE = 0x06
    NORMAL_OPERATION_MODE = 0x07
    READ_DEVICE_CONFIGURATION = 0x05
    GET_FIRMWARE_REVISION = 0x00
    CS_FILTERING_TOUCH_BASELINE_RESET = 0x40 # 0b01000000

    def __init__(self, address, busnum=-1, debug=False):
        self.address = address
        self.bus = smbus.SMBus(busnum if busnum >= 0 else 1)
        self.debug = debug

    def errMsg(self):
        print "Error accessing 0x%02X: Check your I2C address" % self.address
        return -1

    def read(self, register_address):
        """
        Parameters:
            register_address - 8 Bit register address designating where to read

        Return Value:
            byte

        Errors:
            none

        Description:
            reads from the Capsense device
            to get the data at that location and returns a byte
        """
        try:
            result = self.bus.read_byte_data(self.address, register_address)
            if self.debug:
                print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
                            (self.address, result & 0xFF, register_address))
            return result
        except IOError, err:
            return self.errMsg()

    def readString(self, register_address, size):
        """
        Parameters:
            register_address - 8 Bit register_address designating where to read
            size - number of bytes to be read

        Return Value:
            results

        Errors:
            none

        Description:
            reads consecutive bytes starting
            from the given register_address 
        """
        try:
            results = self.bus.read_i2c_block_data(self.address, register_address, 
                                                   length)
            if self.debug:
                print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %
                       (self.address, register_address))
            print ' '.join('{:02x}'.format(x) for x in results)
            return results
        except IOError, err:
            return self.errMsg()

#    def readBuffer(self):
#        """
#        Parameters:
#            none
#
#        Return Value:
#            results 
#
#        Errors:
#            none
#
#        Description:
#            Read from the I2C buffer whatever amount of data is available. It is assumed that this
#            buffer was primed in a previous separate command.
#        """
#        try:
#            print "0x%02X" % self.address
#
#            if self.debug:
#                print "I2C: Reading buffer" 
#
#            results = []
#            while(True):
#                result = self.bus.read_byte(self.address)
#                if result == None:
#                    if self.debug:
#                        print ("No more results")
#                    
#                    break;
#                    if self.debug:
#                        print ("Read result 0x%02X: " % result)
#                    
#            results.append(result)
#
#            if self.debug:
#                print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %
#                       (self.address, register_address))
#                print ' '.join('{:02x}'.format(x) for x in results)
#            return results
#
#        except IOError, err:
#            return self.errMsg()

    def write(self, register_address, data):
        """
        Parameters:
            register_address - 8 Bit register_address designating were to write
            data - Data to be written

        Return Value:

        Errors:

        Description:
            writes a byte to specified register_address

        """
        try:
            self.bus.write_byte_data(self.address, register_address, data)
            if self.debug:
                print "I2C: Wrote 0x%02X to register 0x%02X" % (data, register_address)
        except IOError, err:
            return self.errMsg()

    def writeString(self, register_address, data):
        """
        Parameters:
            register_address - 8 Bit register_address designating were to write
            data - Data to be written

        Return Value:
            none

        Errors:
            none

        Description:
            Writes a string of bytes to
            specified register_address. If amount of bytes is above 64 the data
            will automaticly be truncated.

        """
        try:
            if self.debug:
                print "I2C: Writing list to register 0x%02X:" % register_address
                print ' '.join('{:02x}'.format(x) for x in results)

            if len(data) > 64:
                data = data[:64]

            self.bus.write_i2c_block_data(self.address, register_address, data)
        except IOError, err:
            return self.errMsg()

    def changeDeviceAddress(self, new_address):
        """
        Parameters:
            new_address - 7 Bit new device address to set
            
        Return Value:
            none

        Errors:
            none

        Description:
            Sends command to device to unlock the address register, change the address
            value, and re-lock the register.

        """

        self.writeString(CypressCapsense_I2C.CSE_I2C_DEV_LOCK, unlock, 3)
        # ORed with MSB 1 to set open drain
        self.write(CypressCapsense_I2C.CSE_I2C_ADDR_DM, (0x80|new_address))
        self.writeString(CypressCapsense_I2C.CSE_I2C_DEV_LOCK, lock, 3)
        self.address = new_address

    def setupDevice(self, gpio=0x0, capsense=0x1F1F): #, slider_buttons=[]):
        """
        Parameters:
            gpio - 16 bits to turn on as GPIO xxxBBBBBxxxBBBBB
                   (LSB 8 bits (LSB 5 bits) for GPIO0, MSB 8 bits (LSB 5 bits) GPIO1)
            capsense - 16 bits to turn on as Capsense xxxBBBBBxxxBBBBB
                       (LSB 8 bits (LSB 5 bits) for GPIO0, MSB 8 bits (LSB 5 bits) GPIO1)

        Return Value:
            none

        Errors:
            If the pin settings conflict, return false

        Description:
            Sets the pins to be used as capsense or GPIO on ports 0 and 1. A pin may not be
            both capsense and gpio at the same time.

        """
        gpio0 = (gpio & 0xFF) # LSB
        gpio1 = (gpio >> 8) # MSB

        capsense0 = (capsense & 0xFF) # LSB
        capsense1 = (capsense >> 8) # MSB

        # check for error condition!
        if ((gpio0 & capsense0 > 0x00) or (gpio1 & capsense1 > 0x00)):
            return false

        self.write(CypressCapsense_I2C.CSE_COMMAND_REG, SETUP_OPERATION_MODE)

        # wipe the previous setting.
        self.write(CypressCapsense_I2C.CSE_GPIO_ENABLE0, 0x00)
        self.write(CypressCapsense_I2C.CSE_GPIO_ENABLE1, 0x00)
        self.write(CypressCapsense_I2C.CSE_CS_ENABLE0, 0x00)
        self.write(CypressCapsense_I2C.CSE_CS_ENABLE1, 0x00)
        self.write(CypressCapsense_I2C.CSE_GPIO_ENABLE0, gpio0)
        self.write(CypressCapsense_I2C.CSE_GPIO_ENABLE1, gpio1)
        self.write(CypressCapsense_I2C.CSE_CS_ENABLE0, capsense0)
        self.write(CypressCapsense_I2C.CSE_CS_ENABLE1, capsense1)

        # set some sensible defaults
        self.write(CypressCapsense_I2C.CSE_CS_OTH_SET, 
            (CypressCapsense_I2C.CSE_OTH_SET_DISABLE_EXT_CAP | 
            CypressCapsense_I2C.CSE_OTH_SET_SENSOR_RESET | 
            CypressCapsense_I2C.CSE_OTH_SET_CLOCK_IMO))
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_00, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_01, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_02, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_03, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_04, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_10, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_11, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_12, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_13, 15)
        self.write(CypressCapsense_I2C.CSE_CS_IDAC_14, 15)

        # TODO - setup sliders
        #   look at the documentation for CS_SCAN_POS and CS_SLID_CONFIG
        #for i in range(len(slider_buttons)):
        #    self.write(slider_buttons[i], i)

        self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.STORE_CURRENT_CONFIGURATION_TO_NVM)
        self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.RECONFIGURE_DEVICE)
        self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.NORMAL_OPERATION_MODE)

        return true;

    def fetchTouchStatus(self):
        """
        Parameters:

        Return Value:
            uint16_t - The status of the sensors. Each bit being on/off

        Errors:
            none

        Description:
            Fetches the touch true/false status from the sensors

        """
        try:
            if self.debug:
                print "I2C: fetching touch status from registers 0x%02X and 0x%02X:" % \
                (CypressCapsense_I2C.CSE_CS_READ_STATUS0, CypressCapsense_I2C.CSE_CS_READ_STATUS1)


            tmp = self.read(CypressCapsense_I2C.CSE_CS_READ_STATUS0)
            #print "0x%02X" % tmp
            
            tmp2 = self.read(CypressCapsense_I2C.CSE_CS_READ_STATUS1)
            #print "0x%02X" % tmp2

            tmp3 = (tmp << 8) | (tmp2)

            if self.debug:
                print tmp3

        except IOError, err:
            return self.errMsg()


        return tmp3

    def fetchRawCounts(self, port, sensor):
        """
        Parameters:
            port - Which port to query (0 or 1)
            sensor - Which sensor to query (0-4)

        Return Value:
            uint16_t - The raw count of the sensor.

        Errors:
            If port > 1, or sensor > 4, return 0

        Description:
            Fetches the raw count values from the sensor

        """
        capsensePort = port
        capsenseSensor = sensor

        if (port > 255):
            capsenseSensor = ( port >> 8 )
            capsensePort = 1

        port_sensor_select = (capsensePort << 7) | (capsenseSensor)

        try:
            if self.debug:
                print "I2C: fetching raw count from register 0x%02X, port %d, sensor %d:" % (CypressCapsense_I2C.CSE_CS_READ_BUTTON, port, sensor)  

            self.write(CypressCapsense_I2C.CSE_CS_READ_BUTTON, port_sensor_select)

            tmp = (self.read(CypressCapsense_I2C.CSE_CS_READ_RAWM)) << 8
            tmp |= self.read(CypressCapsense_I2C.CSE_CS_READ_RAWL)

            if self.debug:
                print tmp

            return tmp
        except IOError, err:
            return self.errMsg()

    def reset(self):
        """
        Reset the touch sensors baseline value.
        """
        try:
            if self.debug:
                print "I2C: resetting the touch sensor baseline at register 0x%02X with 0x%02X:" % (CypressCapsense_I2C.CSE_CS_FILTERING, CypressCapsense_I2C.CS_FILTERING_TOUCH_BASELINE_RESET)
            self.write(CypressCapsense_I2C.CSE_CS_FILTERING, CypressCapsense_I2C.CS_FILTERING_TOUCH_BASELINE_RESET)
        except IOError, err:
            return self.errMsg()

    def reboot(self):
        """
        Reboot the board.
        """
        try:      
            if self.debug:
                print "I2C: rebooting, at register 0x%02X, with commands 0x%02X, 0x%02X and 0x%02X:" % (CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.SETUP_OPERATION_MODE, 
                               RECONFIGURE_DEVICE, CypressCapsense_I2C.ORMAL_OPERATION_MODE)
            self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.SETUP_OPERATION_MODE)
            self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.ECONFIGURE_DEVICE)
            self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.NORMAL_OPERATION_MODE)
        except IOError, err:
            return self.errMsg()

#    def fetchFirmwareRevision(self):
#        """
#        Fetch the firmware revision
#        """
#        try:
#            if self.debug:
#                print "I2C: fetching the firmware revision at register 0x%02X with 0x%02X:" % (CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.GET_FIRMWARE_REVISION)
#
#            self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.GET_FIRMWARE_REVISION)
#            tmp = self.readBuffer()
#            if self.debug:
#                print ' '.join('{:02x}'.format(x) for x in results) 
#            return tmp
#
#        except IOError, err:
#            return self.errMsg()
#
#    def fetchDeviceInformation(self):
#        """
#        Fetch the configuraiton information
#        """
#        try:
#            if self.debug:
#                print "I2C: fetching configuration information at register 0x%02X with 0x%02X:" % (CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.READ_DEVICE_CONFIGURATION)
#            self.write(CypressCapsense_I2C.CSE_COMMAND_REG, CypressCapsense_I2C.READ_DEVICE_CONFIGURATION)
#            results = self.readBuffer()
#
#            if self.debug:
#                print ' '.join('{:02x}'.format(x) for x in results) 
#
#            return results
#        except IOError, err:
#            return self.errMsg()

if __name__ == '__main__':
    try:
        bus = CypressCapsense_I2C(address=0)
        print "Default I2C bus is accessible"
    except:
        print "Error accessing default I2C bus"
