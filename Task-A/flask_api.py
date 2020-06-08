"""
Contains the database schema to allow mapping to the database table.
"""
from flask import Flask, Blueprint, request, jsonify, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import extract
import flask
import json, requests
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from forms import RepairsForm
from datetime import date, time
from app import site
from passlib.hash import sha256_crypt

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Car(db.Model):
    """
    The database schema for the Car table.
    """
    __tablename__ = "Car"
    CarID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Make = db.Column(db.Text)
    Type = db.Column(db.Text)
    Location = db.Column(db.Text)
    Color = db.Column(db.Text)
    Seats = db.Column(db.Text)
    CostPerHour = db.Column(db.Text)
    Status = db.Column(db.Text)

    def __init__(self, Make, Type, Location, Color, Seats,Status, CostPerHour, CarID=None):
        self.CarID = CarID
        self.Make = Make
        self.Type = Type
        self.Location = Location
        self.Color = Color
        self.Seats = Seats
        self.CostPerHour = CostPerHour,
        self.Status = Status


class User(db.Model):
    """
    The database schema for the User table.
    """
    column_list = ('FirstName','LastName','UserName','Email','Role')
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    UserName = db.Column(db.Text)
    Email = db.Column(db.Text)
    Role = db.Column(db.Text)
    credentials = db.Column(db.JSON)
    DeviceAddress = db.Column(db.Text)

    def __init__(self, FirstName, LastName, UserName, Email, Role, DeviceAddress, UserID=None):
        self.UserID = UserID
        self.FirstName = FirstName
        self.LastName = LastName
        self.UserName = UserName
        self.Email = Email
        self.Role = Role
        self.DeviceAddress = DeviceAddress


class Login(db.Model):
    """
    The database schema for the Login table.
    """
    __tablename__ = "Login"
    LoginID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.Text)
    Password = db.Column(db.Text)

    def __init__(self, Password, UserName, LoginID=None):
        self.LoginID = LoginID
        self.UserName = UserName
        self.Password = Password

class Booking(db.Model):
    """
    The database schema for the Booking table.
    """
    __tablename__ = "Booking"
    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PickUpDate = db.Column(db.Date)
    PickUpTime = db.Column(db.Time)
    ReturnDate = db.Column(db.Date)
    ReturnTime = db.Column(db.Time)
    CarID = db.Column(db.Integer)
    UserName = db.Column(db.Text)
    eventId = db.Column(db.Text)

    def __init__(
        self,
        PickUpDate,
        PickUpTime,
        ReturnDate,
        ReturnTime,
        CarID,
        UserName,
        BookingID=None,
    ):
        self.BookingID = BookingID
        self.PickUpDate = PickUpDate
        self.PickUpTime = PickUpTime
        self.ReturnDate = ReturnDate
        self.ReturnTime = ReturnTime
        self.CarID = CarID
        self.UserName = UserName

class Repairs(db.Model):
    """
    The database schema for the Repairs table.
    """
    __tablename__ = "Repairs"
    RepairID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssignedDate = db.Column(db.Date)
    CarID = db.Column(db.Integer)
    UserName = db.Column(db.Text)
    Status = db.Column(db.Text)

    def __init__(
        self,
        AssignedDate,
        CarID,
        UserName,
        Status,
        RepairID=None,
    ):
        self.RepairID = RepairID
        self.AssignedDate = AssignedDate
        self.Status = Status
        self.CarID = CarID
        self.UserName = UserName

class RepairsSchema(ma.Schema):
    """
    Format Repairs schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("RepairID", "AssignedDate", "Status", "CarID", "UserName")

repairsSchema = RepairsSchema()
repairsSchema = RepairsSchema(many=True)

class CarSchema(ma.Schema):
    """
    Format Car schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")

carsSchema = CarSchema()
carsSchema = CarSchema(many=True)

class UserSchema(ma.Schema):
    """
    Format User schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("UserID", "FirstName", "LastName", "UserName", "Email", "Role","DeviceAddress")

usersSchema = UserSchema()
usersSchema = UserSchema(many=True)

class LoginSchema(ma.Schema):
    """
    Format Login schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("LoginID", "UserName", "Password")

loginSchema = LoginSchema()
loginSchema = LoginSchema(many=True)

class BookingSchema(ma.Schema):
    """
    Format Booking schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = (
            "BookingID",
            "PickUpDate",
            "PickUpTime",
            "ReturnDate",
            "ReturnTime",
            "CarID",
            "UserName",
        )

class BookingDetailsSchema(ma.Schema):
    """
    Format Booking Detail schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = (
            "BookingID",
            "PickUpDate",
            "PickUpTime",
            "ReturnDate",
            "ReturnTime",
            "UserName",
            "CarID",
            "Make",
            "Type",
            "Location",
            "Color",
            "Seats",
            "CostPerHour",
        )

class RepairDetailsSchema(ma.Schema):
    """
    Format Repair Detail schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = (
            "RepairID", 
            "AssignedDate", 
            "Status",
            "UserName",
            "CarID",
            "Make",
            "Type",
            "Location",
            "Color",
            "Seats",
            "CostPerHour",
        )
class BookingModelView(ModelView):
    can_create = False
    column_list = ('PickUpDate','PickUpTime','ReturnDate','ReturnTime','CarID','UserName')

class UserModelView(ModelView):
    column_list = ('FirstName','LastName','UserName','Email','Role')

class CarModelView(ModelView):
    @action('approve', 'Report', 'Are you sure you want to report faults in selected cars?') 
    def action_approve(self, ids):
        return flask.redirect(url_for('site.reportFault', ids = ids))

bookingSchema = BookingSchema()
bookingSchema = BookingSchema(many=True)

bookingDetailsSchema = BookingDetailsSchema()
bookingDetailsSchema = BookingDetailsSchema(many=True)

repairDetailsSchema = RepairDetailsSchema()
repairDetailsSchema = RepairDetailsSchema(many=True)

# API to get all users
@api.route("/users", methods=["GET"])
def getUsers():
    """
    Retrieve users' information from database.
    Returns:
        JSON: User information (e.g "UserID", "FirstName", "LastName", "UserName", "Email", "Role")
    """
    users = User.query.all()
    result = usersSchema.dump(users)
    return jsonify(result)

# API to get all logins
@api.route("/logins", methods=["GET"])
def getLogins():
    """
    Retrieve logins' information from database.
    Returns:
        JSON: User information ("LoginID", "UserName", "Password")
    """
    logins = Login.query.all()
    result = loginSchema.dump(logins)
    return jsonify(result)

# API to get all cars
@api.route("/cars", methods=["GET"])
def getCars():
    """
    Retrieve cars information from database.
    Returns:
        JSON: Car information ("CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")
    """
    cars = Car.query.all()
    result = carsSchema.dump(cars)
    return jsonify(result)

# API to get all Device addresses of all engineers
@api.route("/deviceAddresses", methods=["GET"])
def getdeviceAddresses():
    """
    Retrieve device addresses information from database.
    Returns:
        JSON: User information (e.g "DeviceAddress")
    """
    users = User.query.add_column("DeviceAddress").filter_by(Role = 'Engineer').all()
    result = usersSchema.dump(users)
    return jsonify(result)
    
# API to get pending repairs by engineer's username
@api.route("/pendingRepairsByUsername/<username>", methods=["GET"])
def getPendingRepairsByUsername(username):
    """
    Get all pending repairs by username from database.

    Returns:
        JSON: Repairs information ("RepairID", "AssignedDate", "Status", "CarID", "UserName")
    """
    repairs = Car.query.join(
    Repairs, Car.CarID == Repairs.CarID).add_columns(
            Repairs.RepairID,
            Repairs.AssignedDate,
            Repairs.Status,
            Repairs.CarID,
            Car.CarID,
            Car.Make,
            Car.Type,
            Car.Location,
            Car.Color,
            Car.Seats,
            Car.CostPerHour,
        ).filter(Repairs.UserName == username, Repairs.Status == 'Pending')
    result = repairDetailsSchema.dump(repairs)
    return jsonify(result)

# API to get all repairs by engineer's username
@api.route("/repairsByUsername/<username>", methods=["GET"])
def getRepairsByUsername(username):
    """
    Get all repairs by username from database.

    Returns:
        JSON: Repairs information ("RepairID", "AssignedDate", "Status", "CarID", "UserName","Make","Type","Color","Seats","Location","CostPerHour")
    """
    repairs = Car.query.join(
    Repairs, Car.CarID == Repairs.CarID).add_columns(
            Repairs.RepairID,
            Repairs.AssignedDate,
            Repairs.Status,
            Repairs.CarID,
            Car.CarID,
            Car.Make,
            Car.Type,
            Car.Location,
            Car.Color,
            Car.Seats,
            Car.CostPerHour,
        ).filter(Repairs.UserName == username)
    result = repairDetailsSchema.dump(repairs)
    return jsonify(result)

# API to get engineer profile by username
@api.route("/engineer/<username>", methods=["GET"])
def getEngineerByUsername(username):
    """
    Retrieve engineer' information from database.
    Returns:
        JSON: User information (e.g "UserID", "FirstName", "LastName", "UserName", "Email", "Role")
    """
    users = User.query.filter(User.UserName == username )
    result = usersSchema.dump(users)
    response = requests.get(
        flask.request.host_url + "/repairsByUsername/" + username
    )
    data = json.loads(response.text)
    print(len(data))
    result[0]['Number of repairs assigned'] = len(data)
    result[0]['Repair data'] = data
    jsonResult = jsonify(result)
    
    return jsonResult

# API to assign faulty cars
@api.route("/reportFaults", methods=["GET", "POST"])
def reportFaults():
    """
    Report faulty cars into the database.

    Returns:
        JSON: "message": "This email is already registered with another account"/"This username is already taken"/"Success"
    """
    data = request.get_json(force=True)

    engineerName = data["engineerName"]
    carIds = data["carIds"]
    for x in carIds:
        newRepair = Repairs(
            CarID=x,
            UserName=engineerName,
            AssignedDate=date.today().isoformat(),
            Status="Pending"
        )
        db.session.add(newRepair)
    db.session.commit()
    return jsonify({"message": "Success"})


# API to login user
@api.route("/loginUser", methods=["GET", "POST"])
def checkLogin():
    """
    Retrieve login information from database and verify login details based on username and password. 

    Returns:
        JSON: "message": "Invalid username or password"/"Success"
    """
    data = request.get_json(force=True)
    user = Login.query.filter_by(UserName=data["username"]).first()
    if user:
        if sha256_crypt.verify(data["password"], user.Password):
            userRole = (User.query.filter_by(UserName=data["username"]).first()).Role
            return jsonify({"message": "Success", "userRole": userRole})
    return jsonify({"message": "Invalid username or password"})
