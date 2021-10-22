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

    # Rejected is to check whether or not we rejected the payload, so that
    # when we get to the 'finally' portion of our try, we don't attempt to
    # close the cursor or conn as we never created them in the first place
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
        _password = _json['password']

        # If we have all of these things, then let's go ahead and add a new uer to the database
        if _username and _firstname and _lastname and _email and _passconfirmed and _password and request.method == 'POST':
            # Let's check our payload for improper values
            if check_payload(_username) or check_payload(_firstname) or check_payload(_lastname) or check_payload(_email) or check_payload(_password):
                # Check Payload returned true, so we have malicious values in our data
                # Return status code 418: I'm a teapot.
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
                rejected = True
                message = {
                    'status': 418,
                    'message': 'Im a teapot. Go away',
                }
                response = jsonify(message)
                response.status_code = 418
                return response

            if _passconfirmed != True:
                # The password was not confirmed prior to being sent to us?
                # Return status code 400: Bad Request
                rejected = True
                message = {
                    'status': 400,
                    'message': 'Password was not confirmed',
                }
                response = jsonify(message)
                response.status_code = 400
                return response

            # Create the SQL query
            sqlQuery = 'CALL sp_register(%s, %s, %s, %s, %s, %s, @registered, @message)'
            bindData = (_username, _password, _passconfirmed, _firstname, _lastname, _email)

            # Make a new connection to the MySQL server
            conn = mysql.connect()
            cursor = conn.cursor()

            # Execute the query and commit it the database
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            # Get the updated variables from the procedure and check them
            cursor.execute('SELECT @registered, @message')
            data = cursor.fetchall()    # data = ((0, 'Username already exists!'),)

            # First value is registered
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

            # Okay so we didn't have any issues, so let's let the client know
            message = {
                'status': 200,
                'message': 'User added successfully!',
            }

            # Put that into a json object and set the status 200: OK
            response = jsonify(message)
            response.status_code = 200

            # Return the status to the client
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
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Define a route to list all registered users.
@app.route('/api/users')
def users():
	try:
        # Make a new connection to the MySQL server
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Select all but sensitive data (password) from the database
		cursor.execute("SELECT username, email, firstName, lastName FROM user")

        # Get all rows retrieved, add them to the response and return
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
		print(e)
	finally:
        # If we've made it here, then we successfully executed our try
        # Now we can close our cursor and connection
		cursor.close()
		conn.close()

# Define a route to get data from our random table
@app.route('/api/random')
def random():
    try:
        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Select name and email from the random table
        cursor.execute('SELECT name, email FROM random')

        # Add that data to the response and return
        randomRows = cursor.fetchall()
        response = jsonify(randomRows)
        response.status_code = 200
        return response
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        print(e)
    finally:
        # If we've made it here, then we successfully executed our try
        # Now we can close our cursor and connection
        cursor.close()
        conn.close()

# Get data about a specific user
# TODO: SQL INJECTION / SECURITY PROTECTIONS
@app.route('/api/user/<string:username>')
def user(username):
    rejected = False

    # First, let's make sure our payload doesn't contain anything malicious
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
        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Get the requested data
        cursor.execute("SELECT username, email, firstName, lastName FROM user WHERE username =%s", username)

        # Fetch only one row from the return
        userRow = cursor.fetchone()

        # Add that row to our response and return
        response = jsonify(userRow)
        response.status_code = 200
        return response
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        print(e)
    finally:
        if rejected == False:
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Delete a user from the table
@app.route('/api/delete/<string:username>')
def delete(username):
    rejected = False
    response = ''
    try:
        # First, let's make sure our payload doesn't contain anything malicious
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

        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor()

        # Create the SQL query
        sqlQuery = 'DELETE FROM user WHERE username=%s'
        bindData = (username,)

        # Execute the query and commit the changes
        cursor.execute(sqlQuery, bindData)
        conn.commit()

        # Send a message to the client letting them know all went well.
        message = {
            'status': 200,
            'message': 'User ' + username + ' deleted successfully!',
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        print(e)
    finally:
        if rejected == False:
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Initializes a new database - to be used when create databse button is clicked
@app.route('/api/initializedb')
def initializedb():
    try:
        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor()

        # We are initializing a new table, 'random', not 'user', so the
        # procedures declared in the users SQL file won't be dropped
        # We're going to open the file with the SQL code to create the random table
        # and execute each line found in it
        for line in open("/Users/sabra/go/src/comp-440/sql/createdb.sql"):
            cursor.execute(line)

        # Create our response to the client and return it
        message = {
            'status': 200,
            'message': 'Database successfully initialized!',
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        print(e)
    finally:
        # If we've made it here, then we successfully executed out try
        # Now we can close our cursor and connection
        cursor.close()
        conn.close()

# Route for logging in?
@app.route('/api/login', methods=["GET", "POST"])
def login():
    response = ''
    rejected = False
    try:
        # Read the payload data from the request and save the values we need
        # Usually a javascript object sent with the fetch call
        _json = request.json

        _username = _json['username']
        _password = _json['password']

        # If we have all of these things, then we wanna try and log the user in
        if _username and _password and request.method == 'POST':
            # First, let's make sure our payload doesn't contain anything malicious
            if check_payload(_username) or check_payload(_password):
                # Check Payload returned true, so we have some malicious data
                # Return status code 418: I'm a teapot.
                rejected = True
                message = {
                    'status': 418,
                    'message': 'Im a teapot. Go away',
                }
                response = jsonify(message)
                response.status_code = 418
                return response

            # Our payload was fine, let's create a new SQL query with it then
            sqlQuery = 'CALL sp_login(%s, %s, @userConfirmed, @passConfirmed)'
            bindData = (_username, _password)

            # Make a new connection to the MySQL server
            conn = mysql.connect()
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(sqlQuery, bindData)
            cursor.execute('SELECT @userConfirmed, @passConfirmed')
            data = cursor.fetchall()

            # Check if the username was confirmed
            if data[0][0] == False:
                rejected = True
                # Username was not confirmed! Don't let them log in
                message = {
                    'status': 409,
                    'message': 'Invalid username given',
                }
                response = jsonify(message)
                response.status_code = 409
                return response

            # Check if our password was confirmed
            if data[0][1] == False:
                # Password was not confirmed! Don't let them log in
                message = {
                    'status': 409,
                    'message': 'Invalid password given',
                }
                response = jsonify(message)
                response.status_code = 409
                return response

            # Both values were good, let's let the client know
            message = {
                'status': 200,
                'message': 'User successfully logged in',
            }
            response = jsonify(message)
            response.status_code = 200
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
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
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
    app.run(host='127.0.0.1', port='5555', debug=True)
