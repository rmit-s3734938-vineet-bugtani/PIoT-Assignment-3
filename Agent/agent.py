import sys, os, json, time
import bluetooth
import socketio
import cv2
from pyzbar.pyzbar import decode
from os.path import exists
from os import system, name

class agentClient:
    ip = None
    carID = None

    def __init__(self):
        self.sioc = socketio.Client()

    def load_config(self) :
        """ Loads json config from config.json
        """
        try:
            with open("config.json") as f:
                data = json.load(f)
                self.ip = "http://" + data["host"] + ":" + data["port"]
                self.carID = data["carID"]
        except Exception as e:
            print(str(e))
            sys.exit("Error when reading from Json.")
    
    def clear(self) :
        """Clears console so that console is clean initially.
        """
        # for windows 
        if name == 'nt': 
            _ = system('cls') 

        # for mac and linux
        else: 
            _ = system('clear')

    def getUsernameFromQR(self, imageName):
        # This will change - not sure whether mac needs full path or some other issues.
        image = cv2.imread('./QRCodes/' + imageName)
        for barcode in decode(image):
            username = barcode.data.decode('utf-8')
            return username

    def connect(self):
        self.sioc.connect(self.ip)
            
    def displayMenu(self):
        self.clear()
        print("Engineer Authnetication App")
        print("1. Engineer Bluetooth Scan")
        print("2. QR Code Profile Scan")
        print("3. Exit")
        option = input("Select an option: ")

        # Get maclist for bluetooth authorization
        if option =='1':
            self.sioc.emit('maclist', callback= self.bluetooth_auth)
        # Get engineer profile through QR code
        elif option == '2':
            # Detect image
                imageName = input('Please enter image name: ')
                if os.path.exists('./QRCodes/' + imageName):
                    username = self.getUsernameFromQR(imageName)
                    print(username)
                    time.sleep(5)
                    self.displayMenu()
                    # self.sioc.emit('reset', callback = self.displayMenu)
                else :
                    print("No image found.")
                    time.sleep(1)
                    self.displayMenu()
                    # self.sioc.emit('reset', callback = self.displayMenu)
        # Close program
        elif option == '3':
            self.sioc.disconnect()
            sys.exit()
        else:
            sys.exit("Incorrect Input")
    
    def bluetooth_auth(self, mac_list):
        # Check surrounding devices against authorized mac addresses
        device_address = None
        nearby_devices = bluetooth.discover_devices()
        for mac_address in nearby_devices:
            if mac_address in mac_list:
                device_address = mac_address
                print("Device Found")
        if device_address is not None:
            # Verify engineer authorization for car via device address
            print("Checking engineer authorization")
            auth, name = self.sioc.call('authorize', data=[self.carID, device_address])
            if auth == False:
                print("Engineer " + name + "is not authorized to work on this car")
                print("Returning to menu")
                time.sleep(3)
                self.sioc.emit('reset', callback = self.displayMenu)
            else:
                print("Hello engineer " + name)
                print("Device address ==", device_address)
                print("You are authorized to perform maintenance on this car")
                print("Car unlocked, press enter when finished with maintenance")
                input()
                self.sioc.emit('reset', callback = self.displayMenu)
        else:
            print("Authorized device not found")
            self.sioc.emit('reset', callback = self.displayMenu)


if __name__ == "__main__":
    agent = agentClient()
    agent.load_config()
    agent.connect()
    agent.displayMenu()