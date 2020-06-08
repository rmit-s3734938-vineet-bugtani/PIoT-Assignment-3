import MySQLdb


class DatabaseUtils:
    # Clone of DB from second assignment.
    HOST = "35.244.76.61"
    USER = "root"
    PASSWORD = "abc123"
    DATABASE = "CarBookingApp"

    def __init__(self, connection=None):
        if connection == None:
            connection = MySQLdb.connect(
                DatabaseUtils.HOST,
                DatabaseUtils.USER,
                DatabaseUtils.PASSWORD,
                DatabaseUtils.DATABASE,
            )
        self.connection = connection

    def close(self):
        """
        Closes the database connection. 
        """
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
    def createTables(self):
        """
        Create database tables if tables do not exists
        """
        with self.connection.cursor() as cursor:
            # cursor.execute("drop table if exists Repairs")
            cursor.execute(
                """
            create table if not exists Repairs (
                RepairID int not null auto_increment,
                CarID int not null,
                UserName text not null,
                AssignedDate date not null,
                Status text not null,
                constraint PK_Repair primary key (RepairID)
                )"""
            )
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('Micheal','Woods','mWoods','micheal.woods@gmail.com','Engineer')")
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('Jordan','Ponting','jPonting','jordan.ponting@gmail.com','Engineer')")
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('Paul','Adams','pAdams','paul.adams@gmail.com','Engineer')")
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('Peter','Cooper','pCooper','peter.cooper@gmail.com','Engineer')")
            # cursor.execute("insert into User (FirstName,LastName,UserName,Email,Role) values ('John','Stocks','jStocks','john.stocks@gmail.com','Engineer')")

            # cursor.execute("delete from Repairs")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (1,'mWoods','2020-01-26','Done')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (2,'jStocks','2020-01-26','Done')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (3,'mWoods','2020-02-26','Done')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (4,'pAdams','2020-02-26','Done')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (2,'mWoods','2020-06-26','Pending')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (3,'mWoods','2020-06-26','Pending')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (4,'mWoods','2020-06-26','Pending')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (8,'jPonting','2020-06-26','Pending')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (12,'pCooper','2020-06-26','Pending')")
            # cursor.execute("insert into Repairs (CarID,UserName,AssignedDate,Status) values (13,'jPonting','2020-06-26','Pending')")

            # cursor.execute("insert into Booking (PickUpDate,PickUpTime,ReturnDate,ReturnTime,CarID,UserName) values ('2020-04-27','01:00:00','2020-04-27','01:00:00','1','s3734938')")
            # cursor.execute("insert into Booking (PickUpDate,PickUpTime,ReturnDate,ReturnTime,CarID,UserName) values ('2020-04-27','01:00:00','2020-04-27','01:00:00','2','s3734938')")
            # cursor.execute("insert into Booking (PickUpDate,PickUpTime,ReturnDate,ReturnTime,CarID,UserName) values ('2020-04-27','01:00:00','2020-04-27','01:00:00','3','s3734938')")
            # cursor.execute("insert into Booking (PickUpDate,PickUpTime,ReturnDate,ReturnTime,CarID,UserName) values ('2020-04-27','01:00:00','2020-04-27','01:00:00','4','s3734938')")
            # cursor.execute("insert into Booking (PickUpDate,PickUpTime,ReturnDate,ReturnTime,CarID,UserName) values ('2020-04-27','01:00:00','2020-04-27','01:00:00','5','s3734938')")

            # cursor.execute("insert into Login (UserName,Password) values ('mWoods','$5$rounds=535000$ugNI5VuPtJoWv0gM$1vJFgAvtWKxc.NDv9KwkdbtqT7HzZD7JXRLYrKi779D')")
            # cursor.execute("insert into Login (UserName,Password) values ('jPonting','$5$rounds=535000$WAPcgbS/EIhKeEov$I5C1SEUPNOvWgz9kFc5o.7mtu1XweB2Kj5XReEXfol2')")
            # cursor.execute("insert into Login (UserName,Password) values ('pAdams','$5$rounds=535000$ATnxcfP11e24E4ih$fXn2YdgzykXx9FXbkIXl/1.WRAo6EbnzQ5eKsfYu7A3')")
            # cursor.execute("insert into Login (UserName,Password) values ('pCooper','$5$rounds=535000$yTSVW8g5Nhxat10H$Y5/cH.sFJ8qeW2i7WCNBA60MwPavObhmFkdw0lg5Nt7')")
            # cursor.execute("insert into Login (UserName,Password) values ('jStocks','$5$rounds=535000$Xhqgz7DeaOT/sr56$1IO0ir/W9wdVlnXRcCoRjSaHzxkZ0UFALh96jlun6Q9')")
           
        self.connection.commit()

    