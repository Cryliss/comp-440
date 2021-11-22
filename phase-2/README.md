# comp-440

Repository for COMP 440: Database Design Group Project

## Group Members
Sabra Bilodeau  
Faizan Hussain  
Shawn Morrison  


# INSTRUCTIONS FOR LOCAL HOSTING

## MySQL SERVER
ON YOUR COMPUTER, YOU MUST HAVE A MYSQL SERVER SETUP IN THE FOLLOWING MANNER:

### TERMINAL
*These instructions are only for Mac users, apologies.*

Open up a new terminal window and login into your MySQL server as root.  
An example of how to do that: `/usr/local/mysql/bin/mysql -u root -p`

Once logged in, run the following commands, one at a time.  

```sql
CREATE DATABASE blogger;

USE blogger;

SOURCE /path/to/your/users.sql;
SOURCE /path/to/your/blogs.sql;
SOURCE /path/to/your/blog.sql;

CREATE USER comp440 IDENTIFIED BY 'pass1234';  
GRANT CREATE, DROP, DELETE, INSERT, SELECT, UPDATE ON blogger.* TO  'comp440'@'localhost';
```

### MySQL Workbench
Create a new schema blogger.  

Create a new user `comp440` with the password `pass1234` and grant the privileges `CREATE`, `DROP`, `DELETE`, `INSERT`, `SELECT`, `UPDATE` to the user for the database.  
[Help on Users and Privileges](https://dev.mysql.com/doc/workbench/en/wb-mysql-connections-navigator-management-users-and-privileges.html)

Open up the `user.sql` file, found in `phase-2/sql/users.sql` and execute it using the lightning bolt. [Nothing tells you it's done, just assume it's done.]

Open up the `blogs.sql` file, found in `phase-2/sql/blogs.sql` and execute it using the lightning bolt.

Open up the `blog.sql` file, found in `phase-2/sql/blog.sql` and execute it using the lightning bolt.

## PYTHON SERVER 

### MAC -- TERMINAL
1. Create an isolated Python environment in a directory external to your project and activate it:

  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

2. Navigate to your project directory and install dependencies:

  ```bash
  cd YOUR_PROJECT_PATH
  pip install -r requirements.txt
  ```

3. Edit `config.py` to include your MYSQL database login information. [Already set up for comp440, pass1234 so if that's your login, you're fine.]

4. Edit `main.py` line# **408**. Edit it to include the file path for your `blogs.sql` file.

5. Run the application:

  ```bash
  python3 main.py
  ```

6. In your web browser, enter the following address:

  ```bash
  http://127.0.0.1:5555
  ```

### PC -- COMMAND LINE
*Use PowerShell to run your Python packages.*

1. Locate your installation of PowerShell.

2. Right-click on the shortcut to PowerShell and start it as an administrator.

3. Create an isolated Python environment in a directory external to your project and activate it:

  ```bash
  python -m venv env
  env\Scripts\activate
  ```

4. Navigate to your project directory and install dependencies:

  ```bash
  cd YOUR_PROJECT
  pip install -r requirements.txt
  ```

5. Edit `config.py` to include your MYSQL database login information. [Already set up for comp440, pass1234 so if that's your login, you're fine.]

6. Edit `main.py` line# **408**. Edit it to include the filepath for your `blogs.sql` file.

7. Run the application:

  ```bash
  python3 main.py
  ```

8. In your web browser, enter the following address:

  ```bash
  http://127.0.0.1:5555
  ```
