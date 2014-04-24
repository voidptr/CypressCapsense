from distutils.core import setup
setup(name='CypressCapsense_I2C',
      version='0.1.0',
      description='Python module for communicating with Cypress Capsense CY8C201xx capacitive touch sensors over I2C',
      author='Rosangela Canino-Koning',
      author_email='cypresscapsensei2c@voidptr.net',
      url='https://github.com/voidptr/CypressCapsense/',
      license='GPL',
      py_modules=['CypressCapsense_I2C'],
      requires=['smbus']
      )
