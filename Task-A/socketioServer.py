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
    return

# Get engineer profile event
@sios.on('profile')
def get_profile(message):
    return