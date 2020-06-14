"""
app.py
========================
The main flask app for userfront website.
"""

import flask
import json, requests
from forms import RepairsForm, LoginForm
from passlib.hash import sha256_crypt
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView, Admin, BaseView

site = flask.Blueprint("site", __name__)

@site.route("/logout")
def logout():
    """
    Logs user out and ends the session.

    Returns:
        HTML: Redirects client to home page.
    """
    if 'username' in flask.session:
        flask.session.pop('username')
    return flask.redirect(flask.url_for("site.login"))

@site.route("/", methods=["GET", "POST"])
@site.route("/admin/login/", methods=["GET", "POST"])
@site.route("/login", methods=["GET", "POST"])
def login():
    """
    Routes client to the login page and depending on the user type, redirect client to respective home page. If login fails, redirects back to login page.

    Returns:
        HTML: Home page / Login page
    """
    form = LoginForm()
    if 'username' in flask.session:
        flask.session.pop('username')
    if form.validate_on_submit():
        userLoginData = {"username":form.username.data, "password":form.password.data}
        response = requests.post(flask.request.host_url + "/loginUser", json=userLoginData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flask.session["username"] = form.username.data
            userRole = data["userRole"]
            if(userRole == 'Engineer'):
                return flask.redirect(flask.url_for("site.gmaps"))
            elif(userRole == 'Manager'):
                return flask.redirect(flask.url_for("site.graphs"))
            elif(userRole == 'Admin'):
                return flask.redirect(flask.url_for("admin.index"))
        else:
            flask.flash(data["message"], "danger")
            form.username.data = ""
    return flask.render_template("login.html", title="Login", form=form)

@site.route('/graphs', methods=["GET", "POST"])
def graphs():
    """
    Displays graphs containing data retrieved from database if logged in. If client not logged in, routes client back to login page. 

    Returns:
        HTML: Graphs page (dashboard) / login page
    """
    if 'username' in flask.session:
        return flask.render_template('graphs.html')
    else:
        return flask.redirect(flask.url_for("site.login"))

@site.route('/gmaps', methods=["GET", "POST"])
def gmaps():
    """
    Displays google maps containing car location retrieved from database if logged in. If client not logged in, routes client back to login page. 

    Returns:
        HTML: Google maps page with car location / login page
    """
    if 'username' in flask.session:
        response = requests.get(
            flask.request.host_url + "/pendingRepairsByUsername/" + flask.session['username']
        )
        data = json.loads(response.text)
        lats = []
        lngs = []
        for x in data:
            y = json.loads(x["Location"])
            lats.append(y["location"]["lat"])
            lngs.append(y["location"]["lng"])
        return flask.render_template('gmaps.html',lats=lats,lngs=lngs)
    else:
        return flask.redirect(flask.url_for("site.login"))

@site.route("/reportFault", methods=["GET", "POST"])
def reportFault():
    """
    Displays page to report faulty cars if logged in. If client not logged in, routes client back to login page. 

    Returns:
        HTML: Page to report faulty cars / login page
    """
    if 'username' in flask.session:
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
    else:
        return flask.redirect(flask.url_for("site.login"))


def sendNotification(title, body):
    """ 
    Sending notification via pushbullet.
    
    Args:
        title (str) : title of text. \n
        body (str) : Body of text.
    """
    # TODO Personal api token. Remove api token before making repo public.
    ACCESS_TOKEN="o.nTPc8SLF2J2nCkfIJQu4ZLCitYpcN2Fc"
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        print('Something went wrong while sending Pushbullet notification.')
    else:
        print('Pushbullet notification sent.')

class Controller(ModelView):
    def is_accessible(self):
        if 'username' in flask.session:
            return True
        else:
            return False

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        if 'username' not in flask.session:
            return flask.redirect(flask.url_for("site.login"))
        else:
            return self.render('admin/index.html')

        