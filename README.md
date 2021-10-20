# comp-440

Repository for COMP 440: Database Design Group Project

## Group Members
Sabra Bilodeau  
Faizan Hussain  
Shawn Morrison  


# INSTRUCTIONS FOR LOCAL HOSTING

## MAC -- TERMINAL
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

3. Edit `config.py` to include your MYSQL database login information.

4. Run the application:

  ```bash
  python3 main.py
  ```

5. In your web browser, enter the following address:

  ```bash
  http://127.0.0.1:8080
  ```

## PC -- COMMAND LINE
### Use PowerShell to run your Python packages.

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

5. Edit `config.py` to include your MYSQL database login information.

6. Run the application:

  ```bash
  python3 main.py
  ```

7. In your web browser, enter the following address:

  ```bash
  http://127.0.0.1:8080
  ```
