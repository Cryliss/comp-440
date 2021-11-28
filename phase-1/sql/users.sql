-- Before you execute this code, you need to create the database first
-- Here are the commands you need to run to create the database & run this file:

-- CREATE DATABASE university;
-- USE university;
-- SOURCE /Users/sabra/go/src/comp-440/users.sql;

-- 1. Create a database schema
-- The schema of the user table should be:
-- user(username, password, firstName, lastName, email)
-- email should be unique & username is the primary key <- Directly conflicts
-- with #3, saying each username should be comp440, so to address that
-- requirement i made our usernames comp440_firstname

-- Let's drop any previously created versions of user table
DROP TABLE IF EXISTS user;

-- Create new user table
CREATE TABLE user (
    username    varchar(45) NOT NULL,
    password    varchar(45) NOT NULL,
    firstName   varchar(45) NOT NULL,
    lastName    varchar(45) NOT NULL,
    email       varchar(100) NOT NULL
);

-- Add a unique constraint on the email
-- I initally thought email and username would be necesarry,
-- but if we all have 'comp440' as a username it doesn't matter
ALTER TABLE user ADD CONSTRAINT unique_email UNIQUE (email);

-- Make username our primary key
ALTER TABLE user ADD PRIMARY KEY (username);

-- 2. Sign up for a new user with information such as:
-- username, password, password confirmed, first name, last name, email.
-- Duplicate username, and email should be detected and fail the signup.

-- Drop existing procedure
DROP PROCEDURE IF EXISTS sp_register;

-- Create a procedure for user registration
-- Code can be called like so:
-- CALL sp_register('comp440_sabra', 'pass1234', true, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @message);
-- SELECT @registered, @message;
DELIMITER $$
CREATE PROCEDURE sp_register( IN username varchar(100), IN password varchar(45), IN passConfirmed boolean, IN firstName varchar(45), IN lastName varchar(45), IN email varchar(45), OUT registered boolean, OUT message varchar(255))
BEGIN
    DECLARE usr varchar(45) DEFAULT '';
    DECLARE eml varchar(100) DEFAULT '';
    -- Has the password been confirmed?
    IF !passConfirmed THEN
        SET registered = FALSE;
        SET message = 'Password was not confirmed??';
    ELSE
        -- Let's make sure we don't already have a user with this username
        SELECT username INTO usr FROM user u WHERE u.username=username LIMIT 1;
        IF usr != '' THEN
            -- Apparently we do .. lets set our out variables
            SET registered = FALSE;
            SET message = 'Username already exists!';
        ELSE
            -- We do not! Do we already have a user with this email?
            SELECT email INTO eml FROM user WHERE username=usr LIMIT 1;
            IF email = eml THEN
                -- Apparently we do .. lets set our out variables
                SET registered = FALSE;
                SET message = 'Email is already registered!';
            ELSE
                -- Nope! So we're good to go ahead and insert into the database.
                START TRANSACTION;
                INSERT INTO user (username, password, firstName, lastName, email) VALUES ( username, password, firstName, lastName, email);
                COMMIT;

                -- Now let's set our out variables.
                SET registered = TRUE;
                SET message = 'User successfully registered';
            END IF;
        END IF;
    END IF;
END $$
DELIMITER ;

-- Let's add Shawn and Faizan to the table using a traditional transation.
START TRANSACTION;
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_faizan', 'pass1234', 'Faizan', 'Hussain', 'faizan.hussain.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_shawn', 'pass1234', 'Shawn', 'Morrison', 'shawn.morrison.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_sabra', 'pass1234', 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu');
COMMIT;

-- 2. (cont) Unmatching passwords should be detected, as well.

-- Drop existing procedure
DROP PROCEDURE IF EXISTS sp_login;

-- Create a procedure for user login .. This is most likely not correct, as we should be hashing and salting values
-- before they get here but whatever.. This is for practice purposes
-- Code can be called like so:
-- CALL sp_login('comp440_sabra', 'pass1234', @passConfirmed);
-- SELECT @passConfirmed;
DELIMITER $$
CREATE PROCEDURE sp_login( IN username varchar(45), IN password varchar(45), OUT userConfirmed BOOLEAN, OUT passConfirmed BOOLEAN )
    BEGIN
        DECLARE uemail varchar(100) DEFAULT '';
        DECLARE us varchar(45) DEFAULT '';
        SET passConfirmed = FALSE;
        SET userConfirmed = FALSE;

        SELECT email INTO uemail FROM user u WHERE u.username=username;
        IF uemail != '' THEN
            SET userConfirmed = TRUE;
            SELECT username INTO us FROM user u WHERE u.email=uemail AND u.password=password;
            IF us != '' THEN
                SET passConfirmed = TRUE;
            END IF;
        END IF;
    END $$
DELIMITER ;
