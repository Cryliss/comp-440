# PROJECT: PHASE 1
1. 5 Points
- [x] Create a database schema and implement user registration and login so that only a registered user can login into the system. (`users.sql`)  
The schema of the user table should be:  
    `user(username, password, firstName, lastName, email)`
- [x] *username* is the primary key (`ALTER TABLE user ADD PRIMARY KEY (username);`)  
- [x] *email* should be unique (`ALTER TABLE user ADD CONSTRAINT unique_email UNIQUE (email);`)  
- [x] You have to prevent SQL injection attacks (`validation.py`)

2. 5 Points  
- [x] Sign up for a new user with information such as: *username, password, password confirmed, first name, last name, email*. (`sp_register`)  
- [x] Duplicate *username* and *email* should be detected and fail the signup (`sp_register` + constraints)  
- [ ] Unmatching passwords should be detected as well. (*I'm confused on this tbh*)

3. 10 Points
- [x] Implement a button called '**Initialize Database**'.  
- [] When a user clicks it, all necessary tables will be created (or recreated) automatically. (Need JS code to call Python server .. `/api/initializedb`)
- [] All students should use the username "comp440" and password "pass1234" (*Conflicts with PK ????????*)
