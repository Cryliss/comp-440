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
            respone = jsonify(message)
            respone.status_code = 200

            # Close our connection
            cursor.close()
            conn.close()
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        return response

@app.route('/user')
def user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT username, email, firstName, lastName FROM user")
		userRows = cursor.fetchall()
		respone = jsonify(userRows)
		respone.status_code = 200
		return respone
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
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='8080', debug=True)
