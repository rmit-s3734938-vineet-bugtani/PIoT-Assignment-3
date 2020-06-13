from flask import Flask, request, jsonify, render_template
from flask_api import *
from flask_admin import expose, AdminIndexView, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from app import *
from database_utils import DatabaseUtils

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

class LoginView(BaseView):
    """
    Add admin view using the flask_admin package
    """
    @expose('/')
    def index(self):
        return flask.redirect(flask.url_for("site.logout"))

admin = Admin(app, 'Admin Page', index_view=AdminIndex())
admin.add_view(CarModelView(Car,db.session,name='View Cars'))
admin.add_view(UserModelView(User,db.session,name='View Users'))
admin.add_view(BookingModelView(Booking,db.session,name='View Bookings'))
admin.add_view(LoginView(name='Logout', endpoint='/logout'))

if __name__ == "__main__":
    # with DatabaseUtils() as db:
    #     db.createTables()
    app.run(host = "0.0.0.0", debug=True)