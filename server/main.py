import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/add', methods=['GET', 'POST'])
def add():
    response = ''
    try:
        _json = request.json
        _username = _json['username']
        _firstname = _json['firstName']
        _lastname = _json['lastName']
        _email = _json['email']
        _passconfirmed = _json['passConfirmed']

        if _username and _firstname and _lastname and _email and _passconfirmed and request.method == 'POST':
            sqlQuery = "CALL sp_register(%s, %s, %s, %s, %s, @registered, @message)"
            bindData = (_username, _passconfirmed, _firstname, _lastname, _email)
            conn = mysql.connect()

            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            message = {
                'status': 200,
                'message': 'User added successfully!',
            }
            response = jsonify(message)
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        # Close our connection
        cursor.close()
        conn.close()

@app.route('/users')
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

@app.route('/user/<string:username>')
def user(username):
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
		cursor.close()
		conn.close()

@app.route('/delete/<string:username>', methods=['DELETE'])
def delete_emp(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE username =%s", (username,))
        conn.commit()
        response = jsonify('User deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/initializedb')
def initializedb():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        for line in open("/Users/sabra/go/src/comp-440/sql/users2.sql"):
            cursor.execute(line)
        
        response = jsonify('Database successfully initialized!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

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
