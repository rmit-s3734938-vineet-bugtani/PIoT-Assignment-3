from flask_socketio import SocketIO, send, emit
from flask import request
import time
import requests, json

sios = SocketIO()

# Reset agent event
@sios.on('reset')
def handle_reset():
    return

# Get mac address list event
@sios.on('maclist')
def get_maclist():
    response = requests.get(request.host_url + "/deviceAddresses")
    jlist = json.loads(response.text)
    mac_list = []
    for item in jlist:
        if item['DeviceAddress'] != 'None':
            mac_list.append(item['DeviceAddress'])
    return mac_list

# Check engineer authorization event
@sios.on('authorize')
def authorize_engineer(message):
    # Get message variables
    carID = message[0]
    deviceaddress = message[1]
    # Identify engineer based on mac address
    response = requests.get(request.host_url + "/engineer/mac/" + deviceaddress)
    engineer = json.loads(response.text)
    # Check if engineer is registered to work on carID
    response = requests.get(request.host_url + "/pendingRepairsByUsername/" + engineer[0]["UserName"])
    repairs = json.loads(response.text)
    # Return engineer name, true or false
    auth = False
    for item in repairs:
        if carID == str(item['CarID']):
            auth = True
            data = {"RepairID":item['RepairID'], "CarID":item['CarID']}
            requests.post(request.host_url + "/fixcar", json=data)
    return auth, engineer[0]["UserName"]

# Get engineer profile event
@sios.on('qr_profile')
def get_profile(message):
    # Request engineer profile from receieved qr username
    response = requests.get(request.host_url + "/engineer/" + message)
    profile = json.loads(response.text)
    if response.status_code == 404:
        return False, profile
    # Return profile information
    return True, profile