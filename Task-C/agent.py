"""
agent.py
=====================
This script is run on agent raspberry pi.
"""
import cv2
from pyzbar.pyzbar import decode
from os.path import exists
from os import system, name
import time
import sys
import os

class agentClient:

    def getUsernameFromQR(self, imageName):
        # This will change - not sure whether mac needs full path or some other issues.
        image = cv2.imread('/Users/vineet/Documents/PIoT-Assignment-3/Task-C/QRCodes/' + imageName)
        for barcode in decode(image):
            username = barcode.data.decode('utf-8')
            return username
    
    def clear(self) :
        """Clears console so that console is clean initially.
        """
        # for windows 
        if name == 'nt': 
            _ = system('cls') 

        # for mac and linux
        else: 
            _ = system('clear')

    # Display menu on agent pi
    def displayMenu(self) :
        """Display user menu on console.
        """
        self.clear()
        print("Welcome to Agent Car")
        print("1. Enter image id to scan")
        print("3. Exit")
        option = input("Select an option: ")
        # Scan qr image
        if option == "1":
            # Detect image
            imageName = input('Please enter image name: ')
            if os.path.exists('/Users/vineet/Documents/PIoT-Assignment-3/Task-C/QRCodes/' + imageName):
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
        #Close connection, close program
        elif option == "3":
            # self.sioc.disconnect()
            sys.exit()
        else :
            #Bad user input, redirect back to displayMenu
            print("Incorrect input, please choose an option")
            time.sleep(1)
            self.displayMenu()
            # self.sioc.emit('reset', callback = self.displayMenu)
    
if __name__ == "__main__":
    agent = agentClient()
    agent.displayMenu()