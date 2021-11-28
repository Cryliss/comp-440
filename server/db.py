import pymysql
from config import mysql

# Function for performing update queries to the database.
def updatedb(sqlQuery, bindData):
    # Make a new connection to the MySQL server
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        #cursor.execute(charsetQuery)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
    except Exception as e:
        message = 'updatedb(' + sqlQuery + str(bindData) + ') err: ' + str(e)
        print(message)
    finally:
        cursor.close()
        conn.close()

# Function to retrieve the procedure results
def procedurecall(sqlQuery, bindData, procQuery):
    # Make a new connection to the MySQL server
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sqlQuery, bindData)
        cursor.execute(procQuery)
        conn.commit()
        data = cursor.fetchall()
        return data
    except Exception as e:
        message = 'procedurecall(' + sqlQuery + ') err: ' + str(e)
        print(message)
    finally:
        cursor.close()
        conn.close()

# Function to perform an SQL query and fetch all results
def queryalldb(sqlQuery, bindData):
    # Make a new connection to the MySQL server
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if bindData == None:
            cursor.execute(sqlQuery)
            conn.commit()
            data = cursor.fetchall()
            return data
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        data = cursor.fetchall()
        return data
    except Exception as e:
        message = 'queryalldb(' + sqlQuery + str(bindData) + ') err: ' + str(e)
        print(message)
    finally:
        cursor.close()
        conn.close()

# Function to perform an SQL query and fetch one row of results
def queryonedb(sqlQuery, bindData):
    # Make a new connection to the MySQL server
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:

        if bindData == None:
            cursor.execute(sqlQuery)
            conn.commit()
            data = cursor.fetchall()
            return data
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        data = cursor.fetchone()
        return data
    except Exception as e:
        message = 'queryonedb(' + sqlQuery + str(bindData) + ') err: ' + str(e)
        print(message)
    finally:
        cursor.close()
        conn.close()

# Function to perform an SQL query and fetch one item from the result
def querydb(sqlQuery, bindData):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        if bindData == None:
            cursor.execute(sqlQuery)
            conn.commit()
            data = cursor.fetchone()
            return data
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        data = cursor.fetchone()
        return data
    except Exception as e:
        message = 'querydb(' + sqlQuery + str(bindData) + ') err: ' + str(e)
        print(message)
    finally:
        cursor.close()
        conn.close()
