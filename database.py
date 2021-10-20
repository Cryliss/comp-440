import mysql.connector
from mysql.connector import errorcode

class Database():
    DB_NAME = 'users'
    SRC_FILE = '/Users/sabra/go/src/comp-440/users.sql'

    def connect_database(config):
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return None
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return None
            else:
                print(err)
                return None
        else:
            print("Successfully connected to the database server.")
        return cnx

    def create_database(cursor):
        try:
            cursor.execute("CREATE DATABSE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
        else:
            print("Successfully created database.")

    def use_database(cursor):
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME
            else:
                print(err)
        else:
            print("Successfully set the database to use.")

    def initialize_database(cursor):
        try:
            cursor.execute("SOURCE {}".format(SRC_FILE))
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("Successfully initialized database.")

def main():
    config = {
        'user': 'sabra',
        'password': 'hA#&kfO5Zx8%',
        'host': '127.0.0.1',
        'raise_on_warnings': True
    }

    cnx = connect_database(config)
    if cnx is None:
        Exit(1)

    cursor = cnx.cursor()

    create_database(cursor)
    use_database(cursor)
    initialize_database(cursor)
