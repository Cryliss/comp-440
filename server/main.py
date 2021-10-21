import pymysql
from app import app
from config import mysql
from validation import check_payload
from flask import jsonify
from flask import flash, request

# Let's create a route for our app that adds a user to our database
# We can get it by using a url like:
# http://127.0.0.1:8080/add
# However, this requires a payload - Go to https://reqbin.com/ to test it out
@app.route('/api/add', methods=['GET', 'POST'])
def add():
    # Create a variable for the response message
    # Unsure why, but if I remove this line, it breaks :D
    response = ''
    rejected = False
    try:
        # Read the payload data from the request and save the values we need
        # Usually a javascript object sent with the fetch call
        _json = request.json

        _username = _json['username']
        _firstname = _json['firstName']
        _lastname = _json['lastName']
        _email = _json['email']
        _passconfirmed = _json['passConfirmed']

        # If we have all of these things, then let's go ahead and add a new uer to the database
        if _username and _firstname and _lastname and _email and _passconfirmed and request.method == 'POST':
            # NEED TO PARSE ITEMS TO CHECK FOR SQL INJECTION
            # NEED TO DO CHECKING I HAD IN SQL CODE HERE COS IT DROPS THAT PROCEDURE WHEN U DROP THAT TABLE

            # Let's check our payload for improper values
            if check_payload(_username) or check_payload(_firstname) or check_payload(_lastname) or check_payload(_email):
                # Check Payload returned true, so we have malicious values in our data
                # Return status code 418: I'm a teapot.
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
                rejected = True
                message = {
                    'status': 418,
                    'message': 'Go away',
                }
                response = jsonify(message)
                response.status_code = 418
                return response

            if _passconfirmed != True:
                # Check Payload returned true, so we have malicious values in our data
                # Return status code 418: I'm a teapot.
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
                rejected = True
                message = {
                    'status': 400,
                    'message': 'Pass was not confirmed',
                }
                response = jsonify(message)
                response.status_code = 400
                return response

            # Create the SQL query
            sqlQuery = 'CALL sp_register(%s, %s, %s, %s, %s, @registered, @message)'
            #sqlQuery = "INSERT INTO user (username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)"
            bindData = (_username, _passconfirmed, _firstname, _lastname, _email)

            # Make a new connection to the MySQL server
            conn = mysql.connect()
            cursor = conn.cursor()

            # Execute the query and commit it the database
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            cursor.execute('SELECT @registered, @message')
            data = cursor.fetchall()

            if data[0][0] == False:
                # We didn't actually register the user when we called sp_register
                # So let's return the reason message to the client
                message = {
                    'status': 409,
                    'message': data[0][1],
                }

                # Put that into a json object and set the status 200: OK
                response = jsonify(message)
                response.status_code = 409
                return response

            # Create a new message object to let the client know what happened
            message = {
                'status': 200,
                'message': 'User added successfully!',
            }

            # Put that into a json object and set the status 200: OK
            response = jsonify(message)
            response.status_code = 200

            # return the status to the client
            return response
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        print(e)
    finally:
        if rejected == False:
            # If we've made it here, then we successfully executed out try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Define a route to list all registered users.
@app.route('/api/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT username, email, firstName, lastName FROM user")
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

# Define a route to get data from our random table
@app.route('/api/random')
def random():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT name, email FROM random')
        randomRows = cursor.fetchall()
        response = jsonify(randomRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Get data about a specific user
# TODO: SQL INJECTION / SECURITY PROTECTIONS
@app.route('/api/user/<string:username>')
def user(username):
    rejected = False
    if check_payload(username):
        # Check Payload returned true, so we have malicious values in our data
        # Return status code 418: I'm a teapot.
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
        rejected = True
        message = {
            'status': 418,
            'message': 'Go away',
        }
        response = jsonify(message)
        response.status_code = 418
        return response
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username, email, firstName, lastName FROM user WHERE username =%s", username)
        userRow = cursor.fetchone()
        response = jsonify(userRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        if rejected == False:
            cursor.close()
            conn.close()

# Delete a user from the table
# TODO: SQL INJECTION / SECURITY PROTECTIONS
@app.route('/api/delete/<string:username>')
def delete_emp(username):
    rejected = False
    if check_payload(username):
        # Check Payload returned true, so we have malicious values in our data
        # Return status code 418: I'm a teapot.
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
        rejected = True
        message = {
            'status': 418,
            'message': 'Go away',
        }
        response = jsonify(message)
        response.status_code = 418
        return response

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE username =%s", (username,))
        conn.commit()
        message = {
            'status': 200,
            'message': 'User ' + username + ' deleted successfully!',
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        if rejected == False:
            cursor.close()
            conn.close()

# Initializes a new database - to be used when create databse button is clicked
@app.route('/api/initializedb')
def initializedb():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # Reading from a SQL file like this did not go as planned
        # so I had to modify my sql code a LOT LOL.
        # Cos I can only read one line at a time this way
        for line in open("/Users/sabra/go/src/comp-440/sql/createdb.sql"):
            cursor.execute(line)
        message = {
            'status': 200,
            'message': 'Database successfully initialized!',
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Basic route for error handling
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='8080', debug=True)
