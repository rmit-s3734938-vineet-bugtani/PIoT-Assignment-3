from flask import Flask, request, jsonify, render_template
import gevent
from gevent import monkey
monkey.patch_all(subprocess=True)
from flask_api import *
from flask_admin import expose, AdminIndexView, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from app import site
from database_utils import DatabaseUtils
from socketioServer import sios

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

HOST = "35.244.76.61"
USER = "root"
PASSWORD = "abc123"
DATABASE = "CarBookingApp"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

sios.init_app(app)

class LoginView(BaseView):
    @expose('/')
    def index(self):
        return flask.redirect(flask.url_for("site.logout"))

admin = Admin(app)
'''
Add admin view using the flask_admin package
'''
admin.add_view(CarModelView(Car,db.session,name='View Cars'))
admin.add_view(UserModelView(User,db.session,name='View Users'))
admin.add_view(BookingModelView(Booking,db.session,name='View Bookings'))
admin.add_view(LoginView(name='Logout', endpoint='/logout'))

if __name__ == "__main__":
    # with DatabaseUtils() as db:
    #     db.createTables()
    #app.run(host = "0.0.0.0", debug=True)
    sios.run(app, host = "192.168.1.225", debug=True)