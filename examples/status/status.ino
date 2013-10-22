/*
Arduinos have internal pullups, but ChipKit does not, so if using a ChipKit board, remember to wire appropriate pullups to the SCK and SDA lines. 
4.7k is a good value for 5v.
*/

#include "Wire.h"
// To use with ATTinyx5 boards, install the TinyWire library, and include it by uncommenting the following line, and comment out the above #include "Wire.h". ATTiny support is EXPERIMENTAL and probably doesn't work.
// This is neccesary because the Arduino Pre-processor does NOT RECOGNIZE #if and #ifdef directives in the main sketch. :P
//#include "TinyWireM.h"

#include <CypressCapsense.h>

#define Port0 0b0000010000000000 //12
#define Port1 0b0000000000010000 //04
#define Port2 0b0000000000001000 //03
#define Port3 0b0000000000000100 //02
#define Port4 0b0000000000000010 //01
#define Port5 0b0000000000000001 //00
#define Port6 0b0000001000000000 //11
#define Port7 0b0000000100000000 //10
#define Port8 0b0001000000000000 //13
#define Port9 0b0000100000000000 //14

byte FoundControllerAddresses[128]; 
byte controllerCount;

// to change the address of the IC, set the below #define to the desired address.
#define ChangeAddress 0

void setup()
{
    #if defined(SerialAvailable)
        Serial.begin(9600);
    #endif
    
    setup_scan();
    
    if (controllerCount > 1)
    {
        #if defined(SerialAvailable)
            Serial.print("Found Controller! address: ");
            Serial.println(FoundControllerAddresses[0]);
        #endif
    }
    
    // only change the first one we find. 
    if (ChangeAddress > 0)
    {
        CypressCapsenseC8YC20.changeDeviceAddress(FoundControllerAddresses[0], ChangeAddress);
        FoundControllerAddresses[0] = ChangeAddress;
    }
}

void loop()
{
    //Serial.println(controllerCount);
    if (controllerCount > 0)
    {
        int status = fetch_sensor_status(FoundControllerAddresses[0]);
        #if defined(SerialAvailable)
            Serial.print("Status: ");
            Serial.println(status);
        #endif
    }
    
}

void setup_scan()
{
    byte addr = 0x00;
    for (int i = 0; i < 100; i++)
    {
        if (test_for_device(addr))
        {

            #if defined(SerialAvailable)
                Serial.print("Found: ");
                Serial.println(i);
            #endif
            
            configure_device(addr);
            
            FoundControllerAddresses[controllerCount] = addr;
            controllerCount++;
        }
        addr++;
    }
}

bool test_for_device(byte addr)
{
    uint8_t buf[1];
    buf[0] = 0xFF;
    
    #if defined(SerialAvailable)
        Serial.print("Testing Address: ");
        Serial.println((int)addr);
    #endif    
    
    // fetch the firmware revision. This will indicate if the device is listening at the default address
    CypressCapsenseC8YC20.fetchFirmwareRevision(addr, buf);
    byte response = buf[0];
    
    if (response != 0xFF)
    {
        #if defined(SerialAvailable)
            Serial.print("FOUND A DEVICE. Version: ");
            byte_array_to_debug_binary_string(buf, 1);
        #endif            
       
        return true;
    }
    return false;
}

#if defined(SerialAvailable)
void byte_array_to_debug_binary_string(uint8_t *buf, int size)
{
    char lByte[9];

    String lContent;

    //Serial.println("Size: " + String(size));

    int i;
    for (i = 0; i < size; i++)
    {
        if ((i % 4) == 0)
            lContent = String(i) + ":   ";

        byte_to_binary_string(buf[i], lByte);

        lContent += String(lByte) + " ";

        if ((i % 4) == 3)
        {
            Serial.println(lContent);
        }   
    }
    if ((i % 4) != 0)
        Serial.println(lContent);
}

void byte_to_binary_string(uint8_t aByte, char *out)
{
        uint8_t lMask = 0x1;
        for (int i = 7; i >= 0; i--)
        {
            if ((aByte & lMask) == 1)
                out[i] = '1';
            else
                out[i] = '0';
            //            out[i] = (aByte & lMask);
            aByte >>= 1;
        }
        out[8] = '\0'; // null char terminator
        //Serial.println(out);
}

#endif

bool configure_device(byte addr)
{
    byte configtarget = addr;
    
//    Debug::debug("CONFIGURING DEVICE @ ");
//    Debug::debugln((int)configtarget);
    // set up the device to read capsense on all ports.
    CypressCapsenseC8YC20.setupDevice(configtarget, 0x0000,
                                      (Port0 | Port1 | Port2 | Port3 | Port4 | Port5 | Port6 | Port7 | Port8 | Port9),
                                      0, NULL);
    
    return true;
}

int fetch_sensor_status(byte addr)
{
    int status = CypressCapsenseC8YC20.fetchTouchStatus(addr);
    CypressCapsenseC8YC20.reset(addr);
    return status;
}

