"""
app.py
========================
The main flask app for userfront website.
"""

import flask
import json, requests

site = flask.Blueprint("site", __name__)

@site.route('/graphs', methods=["GET", "POST"])
def main():
    return flask.render_template('index.html')

@site.route('/getBarGraphData', methods=["GET", "POST"])
def getBookingsByMonth():
    bookings = []
    for x in range(11):
        response = requests.get(
        flask.request.host_url + "/bookings/" + str(x)
    )
        data = json.loads(response.text)
        bookings.append(len(data))
    data = {
        "bookings":bookings
    }
    return data

@site.route('/getPieGraphData', methods=["GET", "POST"])
def getbookingsByCarType():
    bookings = []
    types = ["Sedan","Coupe"]
    for x in types:
        response = requests.get(
        flask.request.host_url + "/bookingsByCarType/" + x
    )
        data = json.loads(response.text)
        bookings.append(len(data))
    data = {
        "bookings":bookings,
        "types":types
    }
    return data

@site.route('/getLineGraphData', methods=["GET", "POST"])
def getRepairsByMonth():
    repairs = []
    for x in range(11):
        response = requests.get(
        flask.request.host_url + "/repairs/" + str(x)
    )
        data = json.loads(response.text)
        repairs.append(len(data))
    data = {
        "repairs":repairs
    }
    return data




