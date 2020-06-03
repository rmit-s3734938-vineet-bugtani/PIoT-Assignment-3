"""
app.py
========================
The main flask app for userfront website.
"""

import flask
import json, requests
from forms import RepairsForm

site = flask.Blueprint("site", __name__)

@site.route('/graphs', methods=["GET", "POST"])
def graphs():
    return flask.render_template('index.html')

@site.route('/gmaps', methods=["GET", "POST"])
def gmaps():
    # Remove this line after login is implemented
    flask.session['username'] = 'pCooper'
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

@site.route("/reportFault", methods=["GET", "POST"])
def reportFault():
    carIds = []
    for x in flask.request.args.getlist('ids'):
       carIds.append(x)
    form = RepairsForm()
    if form.validate_on_submit():
        data = {"engineerName":form.engineerName.data, "carIds":carIds}
        response = requests.post(flask.request.host_url + "/reportFaults", json=data)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flask.flash(data["message"], "success")
            return flask.redirect(flask.url_for('car.index_view'))
        else:
            flask.flash(data["message"], "danger")
    return flask.render_template("reportFaults.html", title="Report Faults", form=form)




