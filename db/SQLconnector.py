"""aids with sql connection"""
#AfterMaps - SQL Connector Module
#Import necessary connector packages/libraries
import mysql.connector as sqlpck
from mysql.connector import errorcode

# Configuration for connecting to database. This is for the basic "aftermaps"
# database, but creditials will be different for main server database.
# Contact Mason for the credentials.
config = {
  'user': 'masterUsername',
  'password': 'TestingPass47',
  'host': 'aftermaps-1.c182aeweubj9.us-east-2.rds.amazonaws.com',
  'database': 'aftermaps',
  'raise_on_warnings': True,
  'auth_plugin':'mysql_native_password'
}

def query_all(query, *parameters):
    """For an SQL query that does not involve pulling information"""
    try:
        cnx = sqlpck.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(query, parameters) #query should be a string
        return cursor.fetchall()
    except sqlpck.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            printd("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            printd("Database does not exist")
        else:
            printd(err)

def query_one(query, *parameters):
    """Query as a string, parameters as a tuple"""
    try:
        cnx = sqlpck.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(query, parameters) #query should be a string
        return cursor.fetchone()
    except sqlpck.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            printd("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            printd("Database does not exist")
        else:
            printd(err)

def query_none(query, *parameters):
    """Query as a string, parameters as a tuple"""
    try:
        printd(f"You've reached query: {parameters}")
        cnx = sqlpck.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(query, parameters) #query should be a string
        cnx.commit()
        printd("Success!")
    except sqlpck.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            printd("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            printd("Database does not exist")
        else:
            printd(err)

def open_sql():
    """To open a connection (hold open)"""
    try:
        cnx = sqlpck.connect(**config)
        cursor = cnx.cursor()
        return cursor
    except sqlpck.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            printd("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            printd("Database does not exist")
        else:
            printd(err)

def open_execute(cursor, query, *parameters):
    """execute a command in open mode"""
    try:
        cursor.execute(query, parameters)

    except sqlpck.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            printd("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            printd("Database does not exist")
        else:
            printd(err)


def close_sql(cnx):
    """close sql connection"""
    cnx.close()

def printd(message):
    """Print messes"""
    """
    prints message
    """
    with open('logfile.txt', 'a') as f:
        f.write(str(message))
