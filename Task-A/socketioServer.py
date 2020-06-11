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
    maclist = []
    for item in jlist:
        if item['DeviceAddress'] != 'None':
            maclist.append(item['DeviceAddress'])
    return maclist

# Get engineer profile event
@sios.on('profile')
def get_profile(message):
    return