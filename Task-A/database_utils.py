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

    