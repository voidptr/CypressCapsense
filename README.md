Cypress Capsense i2c libraries
==============================

Libraries for controlling the Cypress Capsense(R) C8YC201xx series touch sensor chips via i2c.

##Installation

##Arduino

After downloading, rename "Arduino" folder to CypressCapsense and copy to Arduino Libraries folder. Restart Arduino IDE, then open File->Sketchbook->Library->CypressCapsense->status sketch.

##Beaglebone Black Python

Make sure the time on your BBB is correct.
```
$ sudo ntpdate pool.ntp.org
```

To install the prerequisites (Debian):
```
$ sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
```

Download the repository, enter the Beaglebone directory, and run:
```
$ python setup.py install
```

Alternatively, this library is also available in PyPi:
```
$ pip install CypressCapsense_I2C
```


##External Documentation
Backups to the below documents are listed in ReferenceMaterials/

###Cypress Capsense CY8C201xx
http://www.cypress.com/?id=1377

###CY8C201xx Register Reference Guide
http://www.cypress.com/?rID=14664
http://www.cypress.com/?docID=41921

###CY8C201xx Datasheet
http://www.cypress.com/?rID=3912
http://www.cypress.com/?docID=50758

##See Also

###Nan-Wei Gong's Guitar Touch Controller
http://nanweigong.com/blog/?p=102
http://nanweigong.com/blog/wp-content/uploads/2012/06/cy8c20.txt

###Joseph Malloch's Sporano T-Stick
http://josephmalloch.wordpress.com/mumt619/
https://github.com/j4n/sopranino_t-stick/blob/master/firmware/test_capsense/firmware/firmware.pde
