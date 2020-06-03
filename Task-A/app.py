"""
app.py
========================
The main flask app for userfront website.
"""

import flask
import json, requests

site = flask.Blueprint("site", __name__)

@site.route('/graphs', methods=["GET", "POST"])
def graphs():
    return flask.render_template('index.html')

@site.route('/gmaps', methods=["GET", "POST"])
def gmaps():
    # Remove this line after login is implemented
    flask.session['username'] = 'mWoods'
    response = requests.get(
        flask.request.host_url + "/repairsByUsername/" + flask.session['username']
    )
    data = json.loads(response.text)
    lats = []
    lngs = []
    for x in data:
        y = json.loads(x["Location"])
        lats.append(y["location"]["lat"])
        lngs.append(y["location"]["lng"])
    return flask.render_template('gmaps.html',lats=lats,lngs=lngs)




