from app import app
from flaskext.mysql import MySQL

# Need to change this to your local SQL information.
# This should be in an .env file and NOT like this .. TO DO lol.
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sabra'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hA#&kfO5Zx8%'
app.config['MYSQL_DATABASE_DB'] = 'blogger'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'supercalifragilisticexpialidocious'

mysql.init_app(app)
