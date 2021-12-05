import pymysql
from app import app
from app import create_stdmsg, create_response
from config import mysql
from db import updatedb, procedurecall, queryalldb, queryonedb, querydb
from validation import check_payload, check_blogpost
from flask import flash, request, session, redirect, render_template

sqlFile = "/Users/sabra/go/src/comp-440/sql/blogs.sql"

@app.route('/')
def index():
    username = session.get('username')
    if username == None:
        return redirect('login.html', code=302)
    elif session.get('initialized') == None:
        return redirect('start.html', code=302)
    return render_template('home.html')

# Route for logging out the user.
@app.route('/logout')
def logout():
    # Remove the username from the session if its there.
    session.pop('username', None)
    # Comment out this line if you'd like the database to persist after logout
    session.pop('initialized', None)
    return redirect('login.html', code=302)

# Route for the home page
@app.route('/home.html')
def home():
    username = session.get('username')
    if username == None:
        return redirect('login.html', code=302)
    return render_template('home.html')

# Route for the login page
@app.route('/login.html')
def login():
    # Is someone logged in?
    username = session.get('username')
    if username != None:
        # Yep, so let's redirect them to the home screen
        return redirect('home.html', code=302)
    # Nope, let's render the login template
    return render_template('login.html')

# Route for the start page
@app.route('/start.html')
def start():
    username = session.get('username')
    if username == None:
        return redirect('login.html', code=302)
    elif session.get('initialized') != None:
        return redirect('home.html', code=302)
    return render_template('start.html')

# Route for the register page
@app.route('/register.html')
def register():
    # Is someone logged in?
    username = session.get('username')
    if username != None:
        # Yep, so let's redirect them to the home screen
        return redirect('home.html', code=302)
    # Nope, so let's go ahead and render the register template
    return render_template('register.html')

# Route for the queries page
@app.route('/queries.html')
def queries():
    # Is someone logged in?
    username = session.get('username')
    if username == None:
        # Yep, so let's redirect them to the home screen
        return redirect('login.html', code=302)
    # Nope, so let's go ahead and render the register template
    return render_template('queries.html')

# Let's create a route for our app that adds a user to our database
# We can get it by using a url like:
# http://127.0.0.1:8080/add
# However, this requires a payload - Go to https://reqbin.com/ to test it out
@app.route('/api/add', methods=['GET', 'POST'])
def add():
    try:
        # Read the payload data from the request and save the values we need
        # Usually a javascript object sent with the fetch call
        _json = request.body

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
                message = create_stdmsg('Im a teapot. Go away', 418)
                return create_response(message, 418)

            if _passconfirmed != True:
                # The password was not confirmed prior to being sent to us?
                # Return status code 400: Bad Request
                message = create_stdmsg('Password was not confirme', 400)
                return create_response(message, 400)

            # Create the SQL query
            sqlQuery = 'CALL sp_register(%s, %s, %s, %s, %s, %s, @registered, @message)'
            bindData = (_username, _password, _passconfirmed, _firstname, _lastname, _email)

            # Get the updated variables from the procedure and check them
            data = procedurecall(sqlQuery, bindData,'SELECT @registered, @message')    # data = ((0, 'Username already exists!'),)

            # First value is registered
            if data[0][0] == False:
                # We didn't actually register the user when we called sp_register
                # So let's return the reason message to the client
                message = create_stdmsg(data[0][1], 409)
                # Return the response message to the client
                return create_response(message, 409)

            # Okay so we didn't have any issues, so let's let the client know
            message = create_stdmsg('User added successfully!', 200)
            # Return the response message to the client
            return create_response(message, 200)
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        message = 'add: failed to add new user. '+str(e)
        print(message)

# Define a route to list all registered users.
@app.route('/api/users')
def users():
    try:
        # Select all but sensitive data (password) from the database
        userRows = queryalldb("SELECT username, email, firstName, lastName FROM user", None)
        return create_response(userRows, 200)
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        message = 'users: failed to retrieve all users. '+str(e)
        print(message)

# Route for editing .. not tested lol
@app.route('/api/blog/edit')
def editblog():
    try:
        _json = request.json

        _blogid = _json["blogid"]
        _subject = _json["subject"]
        _description = _json["description"]
        _tags = _json["tags"]

        if _blogid and _subject and _description and _tags and request.method=="POST":
            if check_payload(str(_blogid)) or check_blogpost(_subject) or check_blogpost(_description) or check_blogpost(_tags):
                message = create_stdmsg("I'm a teapot. Go away.", 418)
                return create_response(message, 418)

            # Select the creator the blog they want to update
            creator = querydb("SELECT created_by FROM blogs WHERE blogid=%s", _blogid)

            # Make sure our user is the one who made the blog
            user = session.get('username')
            if creator != user:
                message = create_stdmsg("You can't edit a blog post that isn't your own!", 409)
                return create_response(message, 409)

            # Update the database
            sqlQuery = "UPDATE blogs SET subject=%s, description=%s WHERE blogid=%s"
            bindData = (_subject, _description, _blogid)
            updatedb(sqlQuery, bindData)

            # Create the response message
            message = create_stdmsg('Blog post successfully updated.', 200)
            return create_response(message, 200)
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        message = 'editblog: failed to edit blog post. '+str(e)
        print(message)

# Define a route for creating a new blog post
@app.route('/api/newpost', methods=["GET", "POST"])
def newpost():
    try:
        _json = request.json

        _subject = _json["subject"]
        _description = _json["description"]
        _tags = _json["tags"]

        if _subject and _description and _tags and request.method=="POST":
            if check_blogpost(_subject) or check_blogpost(_tags):
                message = create_stdmsg("I'm a teapot. Go away.", 418)
                return create_response(message, 418)

            _poster = session.get('username')
            if _poster == None:
                message = create_stdmsg('User must be signed in to perform this action', 403)
                return create_response(message, 403)

            sqlQuery = 'CALL sp_insertPost(%s, %s, %s, NOW(), %s, @blogid, @message)'
            bindData = (_subject, _description, _poster, _tags)

            # Use updatedb function to perform the procedure call
            data = procedurecall(sqlQuery, bindData, 'SELECT @blogid, @message')
            print(data)
            if data[0][0] == -1:
                message = create_stdmsg(data[0][1], 409)
                return create_response(message, 409)

            message = {
                "blogid": data[0][0],
                "dbmessage": data[0][1],
                "status": 200,
            }
            return create_response(message, 200)
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        message = 'newpost: failed to create a new post. '+str(e)
        print(message)

@app.route('/api/newcomment', methods=["GET", "POST"])
def newcomment():
    try:
        _json = request.json

        _sentiment = _json["sentiment"]
        _description = _json["description"]
        _blogid = _json["blogid"]

        if _sentiment and _description and _blogid and request.method=="POST":
            if check_payload(_sentiment) or check_blogpost(_description):
                message = create_stdmsg("I'm a teapot. Go away.")
                return create_response(message, 418)

            if _sentiment != 'positive' and _sentiment != 'negative':
                message = create_stdmsg("Invalid sentiment provided", 409)
                return create_response(message, 409)

            _poster = session.get('username')
            if _poster == None:
                message = create_stdmsg('User must be signed in to perform this action', 403)
                return create_response(message, 403)

            sqlQuery = 'CALL sp_comment(%s, %s, NOW(), %s, %s, @commentid, @message)'
            bindData = (_sentiment, _description, _blogid, _poster)

            # Use updatedb function to perform procedure call
            data = procedurecall(sqlQuery, bindData, 'SELECT @commentid, @message')

            if data[0][0] == -1:
                message = create_stdmsg(data[0][1], 409)
                return create_response(message, 409)

            message = {
                "message": "Comment id: "+str(data[0][0])+" Db message: "+data[0][1],
                "status": 200,
                "commentid": data[0][0],
            }
            return create_response(message, 200)
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        message = 'newcomment: failed to create new comment. '+str(e)
        print(message)

@app.route('/api/blogs')
def blogs():
    try:
        # Select all from blogs
        blogRows = queryalldb("SELECT * FROM blogs;", None)
        blogs = []
        for b in blogRows:
            bindData = (b['blogid'],)
            tags = queryalldb('SELECT tag FROM blogstags WHERE blogid=%s', bindData)

            tag = ''
            for t in tags:
                if tag == '':
                    tag = '#'+t['tag']
                else:
                    tag = tag+' #'+t['tag']

            comments = queryalldb('SELECT commentid, sentiment, description, cdate, posted_by FROM comments WHERE blogid=%s',bindData)
            blog = {
                "blogid": b['blogid'],
                "subject": b['subject'],
                "description": b['description'],
                "pdate": b['pdate'],
                "created_by": b['created_by'],
                "tags": tag,
                "comments": comments,
            }
            blogs.append(blog)
        return create_response(blogs, 200)
    except Exception as e:
        message = 'blogs: failed to retrieve blogs. '+str(e)
        print(message)

@app.route('/api/comments/<int:blogid>')
def comments(blogid):
    try:
        if check_payload(str(blogid)):
            message = create_stdmsg("I'm a teapot. Go away.", 418)
            return create_response(message, 418)

        # Select all from comments
        commentRows = queryalldb("SELECT * FROM comments WHERE blogid=%s;", blogid)
        return create_response(commentRows, 200)
    except Exception as e:
        message = 'comments(' + str(blogid) + '): failed to retrieve comments on blog. '+str(e)
        print(message)

@app.route('/api/comment/<int:commentid>')
def comment(commentid):
    try:
        if check_payload(str(commentid)):
            message = create_stdmsg("I'm a teapot. Go away.", 418)
            return create_response(message, 418)
        commentRow = queryonedb("SELECT * FROM comments where commentid=%s", commentid)
        return create_response(commentRow, 200)
    except Exception as e:
        message = 'comment(' + str(commentid) + '): failed to retrieve comment. '+str(e)
        print(message)

# Get data about a specific blog
@app.route('/api/blog/<int:blogid>')
def blog(blogid):
    # First, let's make sure our payload doesn't contain anything malicious
    if check_payload(str(blogid)):
        # Check Payload returned true, so we have malicious values in our data
        # Return status code 418: I'm a teapot.
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
        message = create_stdmsg("I'm a teapot. Go away.", 418)
        return create_response(message, 418)
    try:
        # Get the requested data
        blogRow = queryonedb("SELECT * FROM blogs WHERE blogid = %s", blogid)
        commentRows = queryalldb("SELECT * FROM comments WHERE blogid = %s", blogid)

        message = {
            "blog": blogRow,
            "comments": commentRows,
        }
        # Add that row to our response and return
        return create_response(message, 200)
    except Exception as e:
        # Was there some error in our code above?
        # Print it out to the terminal so we can try and debug it
        message = 'blog(' + str(blogid) + '): failed to get blog. '+str(e)
        print(message)

# Delete a user from the table
@app.route('/api/delete/<string:username>')
def delete(username):
    try:
        # First, let's make sure our payload doesn't contain anything malicious
        if check_payload(username):
            # Check Payload returned true, so we have malicious values in our data
            # Return status code 418: I'm a teapot.
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
            message = create_stdmsg("I'm a teapot. Go away.", 418)
            return create_response(message, 418)

        # Create & execute the SQL query
        sqlQuery = 'DELETE FROM user WHERE username=%s'
        bindData = (username,)
        updatedb(sqlQuery, bindData)

        # Send a message to the client letting them know all went well.
        text = 'User' + username + ' deleted successfully'
        message = create_stdmsg(text, 200)
        return create_response(message, 200)
    except Exception as e:
        message = 'delete(' + username + '): failed to delete user. '+str(e)
        print(message)

# Initializes a new database - to be used when create databse button is clicked
@app.route('/api/initializedb')
def initializedb():
    response = ''
    rejected = True
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
        for line in open(sqlFile):
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
        message = create_stdmsg('Database successfully initialized!', 200)
        session['initialized'] = True
        return create_response(message, 200)
    except Exception as e:
        message = 'initializedb: failed to initialize database. '+str(e)
        print(message)
    finally:
        if response != '' and rejected == False:
            # If we've made it here, then we successfully executed out try
            # Now we can close our cursor and connection
            cursor.close()
            conn.close()

# Route for logging in?
@app.route('/api/login', methods=["GET", "POST"])
def loginUser():
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
                message = create_stdmsg("I'm a teapoot. Go away", 418)
                return create_response(message, 418)

            # Our payload was fine, let's create a new SQL query with it then
            sqlQuery = 'CALL sp_login(%s, %s, @userConfirmed, @passConfirmed)'
            bindData = (_username, _password)

            data = procedurecall(sqlQuery, bindData, 'SELECT @userConfirmed, @passConfirmed')
            print(data)
            # Check if the username was confirmed
            if data[0][0] == False:
                # Username was not confirmed! Don't let them log in
                message = create_stdmsg('Username does not exit!', 409)
                return create_response(message, 409)

            # !!!!!! REALLY NEED TO HASH AND SALT OUR PASSWORDS !!!!!!!!!!!!
            # Check if our password was confirmed
            if data[0][1] == False:
                # Password was not confirmed! Don't let them log in
                message = create_stdmsg('Invalid password was given', 409)
                return create_response(message, 409)

            # Both values were good, let's let the client know
            message = create_stdmsg('User successfully logged in', 200)
            session['username'] = _username
            return create_response(message, 200)
        else:
            # Hm, we didn't get anything in our payload, return 404
            return not_found()
    except Exception as e:
        if str(e) == "'cryptography' package is required for sha256_password or caching_sha2_password auth methods":
            # Password was not confirmed! Don't let them log in
            message = create_stdmsg('Invalid password was given', 409)
            return create_response(message, 409)
        message = 'loginUser: failed to login user. '+str(e)
        print(message)

@app.route('/api/userdata', methods=["GET"])
def userdata():
    try:
        if session.get('initialized') == True:
            _username = session.get('username')

            bindData = (_username,)
            dbblogs = queryalldb('SELECT * FROM blogs WHERE created_by=%s',bindData)
            dbhobbies = queryalldb('SELECT hobby FROM hobbies WHERE username=%s',bindData)
            dbfollowing = queryalldb('SELECT leadername AS user FROM follows WHERE followername=%s',bindData)
            dbfollowers = queryalldb('SELECT followername AS user FROM follows WHERE leadername=%s',bindData)

            hobbies = []
            for h in dbhobbies:
                hobbies.append(h["hobby"])

            following = []
            for f in dbfollowing:
                following.append(f["user"])

            followers = []
            for f in dbfollowers:
                followers.append(f["user"])

            blogs = []
            for b in dbblogs:
                bindData = (b['blogid'],)
                tags = queryalldb('SELECT tag FROM blogstags WHERE blogid=%s', bindData)

                tag = ''
                for t in tags:
                    if tag == '':
                        tag = "#"+t['tag']
                    else:
                        tag = tag+' #'+t['tag']

                comments = queryalldb('SELECT commentid, sentiment, description, cdate, posted_by FROM comments WHERE blogid=%s',bindData)

                blog = {
                    "blogid": b['blogid'],
                    "subject": b['subject'],
                    "description": b['description'],
                    "pdate": b['pdate'],
                    "created_by": b['created_by'],
                    "tags": tag,
                    "comments": comments,
                }
                blogs.append(blog)

            userData = {
                "blogs": blogs,
                "hobbies": hobbies,
                "followers": followers,
                "following": following,
            }
            return create_response(userData, 200)
        else:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'userdata: failed to retrieve user data '+str(e)
        print(message)

# PHASE 3 QUERY ROUTES
@app.route('/api/query1', methods=["GET", "POST"])
def query1():
    try:
        _json = request.json
        _creator = _json["created_by"]

        if session.get('initialized') == False:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)

        if _creator and request.method=="POST":
            if check_payload(_creator):
                message = create_stdmsg("I'm a teapoot. Go away", 418)
                return create_response(message, 418)
            sqlQuery = 'SELECT * FROM blogs b WHERE b.created_by=%s AND EXISTS (SELECT * FROM comments c WHERE b.blogid=c.blogid AND c.sentiment="positive")'
            bindData = (_creator,)
            data = queryalldb(sqlQuery, bindData)
            message = {
                "blogs": data,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("You must giver a user name in the query!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query1: failed to retrieve data '+str(e)
        print(message)

@app.route('/api/query2', methods=["GET", "POST"])
def query2():
    try:
        _json = request.json
        _pdate = _json["pdate"]

        if session.get('initialized') == False:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)

        if _pdate and request.method=="POST":
            if check_payload(_pdate):
                message = create_stdmsg("I'm a teapoot. Go away", 418)
                return create_response(message, 418)
            sqlQuery = "SELECT DISTINCT created_by FROM blogs WHERE pdate IN (SELECT pdate FROM blogs WHERE pdate=%s)"
            bindData = (_pdate,)
            data = queryalldb(sqlQuery, bindData)
            users = []
            for user in data:
                users.append(user["created_by"])
            message = {
                "users": users,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("You must giver a post date in the query!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query2: failed to retrieve data '+str(e)
        print(message)

@app.route('/api/query3', methods=["GET", "POST"])
def query3():
    try:
        _json = request.json
        _userx = _json["userx"]
        _usery = _json["usery"]

        if session.get('initialized') == False:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)

        if _userx and _usery and request.method=="POST":
            if check_payload(_userx) or check_payload(_usery):
                message = create_stdmsg("I'm a teapoot. Go away", 418)
                return create_response(message, 418)
            sqlQuery = "SELECT DISTINCT f.leadername FROM follows f INNER JOIN follows f2 ON f2.leadername=f.leadername WHERE f.followername=%s AND f2.followername=%s;"
            bindData = (_userx,_usery)
            data = queryalldb(sqlQuery, bindData)
            users = []
            for user in data:
                users.append(user["leadername"])
            message = {
                "users": users,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("You must giver two usernames in the query!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query3: failed to retrieve data '+str(e)
        print(message)

@app.route('/api/query4')
def query4():
    try:
        if session.get('initialized') == True:
            sqlQuery = "SELECT DISTINCT username FROM user u WHERE NOT EXISTS (SELECT * FROM blogs WHERE created_by=u.username )"
            data = queryalldb(sqlQuery, None)
            users = []
            for user in data:
                users.append(user["username"])
            message = {
                "users": users,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query4: failed to retrieve data '+str(e)
        print(message)

@app.route('/api/query5')
def query5():
    try:
        if session.get('initialized') == True:
            sqlQuery = "SELECT DISTINCT posted_by FROM comments c WHERE sentiment='negative' AND NOT EXISTS (SELECT DISTINCT posted_by FROM comments c2 WHERE c2.sentiment='positive' AND c2.posted_by=c.posted_by)"
            data = queryalldb(sqlQuery, None)
            users = []
            for user in data:
                users.append(user["posted_by"])
            message = {
                "users": users,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query4: failed to retrieve data '+str(e)
        print(message)

@app.route('/api/query6')
def query6():
    try:
        if session.get('initialized') == True:
            sqlQuery = "SELECT DISTINCT created_by FROM blogs WHERE NOT EXISTS(SELECT DISTINCT sentiment FROM comments WHERE comments.sentiment='negative' AND comments.blogid=blogs.blogid)"
            data = queryalldb(sqlQuery, None)
            users = []
            for user in data:
                users.append(user["created_by"])
            message = {
                "users": users,
                "status": 200,
            }
            return create_response(message,200)
        else:
            message = create_stdmsg("Database must be initialized before any data can be retrieved!", 400)
            return create_response(message, 400)
    except Exception as e:
        message = 'query4: failed to retrieve data '+str(e)
        print(message)

# Basic route for error handling
@app.errorhandler(404)
def not_found(error=None):
    text = 'Record not found: ' + request.url
    message = create_stdmsg(text, 404)
    return create_response(message, 404)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5555', debug=True)
