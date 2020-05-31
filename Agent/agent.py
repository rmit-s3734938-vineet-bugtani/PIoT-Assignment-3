import sys, os
import bluetooth
#Menu
mac = "48:59:A4:2B:FB:20"
print("Bluetooth App")
print("1. Scan for bluetooth device")
print("2. Exit")
option = input("Select an option")

if option =='1':
    #Activate bluetooth
    device_address = None
    nearby_devices = bluetooth.discover_devices()
    for mac_address in nearby_devices:
        if mac in mac_address:
            device_address = mac_address
            print("Phone Found")
    if device_address is not None:
        print("Mac address ==", device_address)
    else:
        print("Phone not found")
    #Get List of valid MAC Addresses

    #Detect phone via matching MAC Address

    #Send mac address to server
elif option == '2':
    sys.exit()

else:
    sys.exit("Incorrect Input")

    #Server returns username

    #Car unlocked

    #Ask engineer for QR

    #Scan QR

    #Send QR back to server, server updates car with last engineer encounter based on QR