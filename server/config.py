from app import app
from flaskext.mysql import MySQL

# Need to change this to your local SQL information.
# This should be in an .env file and NOT like this .. TO DO lol.
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'comp440'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass1234'
app.config['MYSQL_DATABASE_DB'] = 'blogger'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'supercalifragilisticexpialidocious'

mysql.init_app(app)
