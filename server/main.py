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
    rejected = True
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

            rejected = False
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
    rejected = True
    response = ''
    try:
        rejected == False
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
        if rejected == False:
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Define a route to get data from our random table
@app.route('/api/advisor')
def random():
    rejected = True
    response = ''
    try:
        rejected = False

        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Select name and email from the advisor table
        cursor.execute('SELECT * FROM advisor')

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
        if rejected == False:
            # If we've made it here, then we successfully executed our try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Get data about a specific user
@app.route('/api/user/<string:username>')
def user(username):
    rejected = True

    # First, let's make sure our payload doesn't contain anything malicious
    if check_payload(username):
        # Check Payload returned true, so we have malicious values in our data
        # Return status code 418: I'm a teapot.
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
        rejected = True
        message = {
            'status': 418,
            'message': "I'm a teapot. Go away",
        }
        response = jsonify(message)
        response.status_code = 418
        return response

    try:
        rejected = False
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
    rejected = True
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

        rejected = False

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
    rejected = True
    response = ''
    try:
        # Make a new connection to the MySQL server
        conn = mysql.connect()
        cursor = conn.cursor()

        rejected = False

        # We are going to re-initialize all the tables except for our users table
        # by using the university-1.sql file, provided by the professor.
        # In order to use this file properly, we need to make sure we don't accidently
        # try to execute lines of code that are just comments, or multiples line long
        # as this will cause an error. The following for loop handles the processing
        # of the file.

        # sql will hold the SQL statement for when we see 'CREATE', as that's usually
        # for 'CREATE TABLE' which always has new lines in it, so we need to add
        # the lines following this to sql, so we can get one string for the full
        # create satement.
        sql = ''

        # waiting is if we are waiting to see a ';' to indicate the statement end.
        waiting = False
        for line in open("/Users/sabra/go/src/comp-440/sql/university-1.sql"):
            # Strip the line of the new line character, '\n'
            line = line.strip()

            # Is this just an empty line?
            if line == '':
                # Yep, move on.
                continue
            elif line[0] == '-' or line[0] == '/':
                # We have a comment here, move on
                continue
            elif line[len(line)-1] == ';' and waiting:
                # We've been waiting for the end of statement character, ';'
                # and now we've found it
                waiting = False         # Set waiting to false
                sql = sql + line        # Add the last line to the statement
                #print(sql)              # Output the statement to the terminal
                cursor.execute(sql)     # Execute the statement
                sql = ''                # Reset our sql variable
                continue                # Move on with the for loop
            elif len(line) > 6:
                # Is the length of the line > 6 (since we want to check up to index 5)?
                if line[0] == 'C' and line[1] == 'R' and line[2] == 'E' and line[3] == 'A' and line[4] == 'T' and line[5] == 'E':
                    # Yep, did the first 5 char spell create? Yep!
                    # We're making a new table then
                    waiting = True      # Set waiting to true.
                    sql = sql + line    # Add the line to the sql variable
                    continue            # Move on with the for loop
                elif waiting:
                    # The length is indeed longer, but we're not a create statement
                    # and we are waiting to be executed
                    sql = sql + line    # Add the line to the sql variable
                    continue            # Move on with the for loop
                else:
                    # The length is indeed longer, but we're not waiting either
                    # Print and execute the command and continue on
                    #print(line)
                    cursor.execute(line)
                    continue
            elif waiting:
                # None of the above are true, but we're waiting
                sql = sql + line        # Add the line to the sql variable
                continue                # Move on with the for loop
            # Nothing above was true, and we're not waiting for an ';'
            # Print the command and execute it.
            #print(line)
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
        if rejected == False:
            # If we've made it here, then we successfully executed out try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Route for logging in?
@app.route('/api/login', methods=["GET", "POST"])
def login():
    response = ''
    rejected = True
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
                    'message': "I'm a teapot. Go away",
                }
                response = jsonify(message)
                response.status_code = 418
                return response

            rejected = False
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
                    'message': 'Username does not exist!',
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
