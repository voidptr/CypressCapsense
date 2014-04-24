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
