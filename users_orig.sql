-- Before you execute this code, you need to create the database first
-- Here are the commands you need to run to create the database & run this file:

-- CREATE DATABASE users;
-- USE users;
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
    username    varchar(255) NOT NULL,
    password    varchar(255) NOT NULL DEFAULT 'pass1234',
    firstName   varchar(255) NOT NULL,
    lastName    varchar(255) NOT NULL,
    email       varchar(255) NOT NULL
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
-- CALL sp_register('comp440_sabra', true, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @message);
-- SELECT @registered, @message;
DELIMITER $$
CREATE PROCEDURE sp_register( IN username varchar(255), IN password varchar(255), IN passConfirmed boolean, IN firstName varchar(255), IN lastName varchar(255), IN email varchar(255), OUT registered boolean, OUT message varchar(255))
BEGIN
    DECLARE usr, eml varchar(255) DEFAULT '';

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
                INSERT INTO user (username, password, firstName, lastName, email) VALUES ( username, DEFAULT, firstName, lastName, email);
                COMMIT;

                -- Now let's set our out variables.
                SET registered = TRUE;
                SET message = 'User successfully registered';
            END IF;
        END IF;
    END IF;
END $$
DELIMITER ;

-- Okay, now that the procedure is defined, let's try calling it, but we want to call
-- it saying that the password is not confirmed so we get an message.
CALL sp_register('comp440_sabra', FALSE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @message);
SELECT @registered, @message;

-- RETURN
-- +-------------+------------------------------+
-- | @registered | @message                     |
-- +-------------+------------------------------+
-- |           0 | Password was not confirmed?? |
-- +-------------+------------------------------+

-- Let's add Shawn and Faizan to the table using a traditional transation.
START TRANSACTION;
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_faizan', 'pass1234', 'Faizan', 'Hussain', 'faizan.hussain.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_shawn', 'pass1234', 'Shawn', 'Morrison', 'shawn.morrison.???@my.csun.edu');
COMMIT;

-- Now let's try adding me again. This time it should work.
CALL sp_register('comp440_sabra', TRUE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @message);
SELECT @registered, @message;

-- RETURN
-- +-------------+------------------------------+
-- | @registered | @message                     |
-- +-------------+------------------------------+
-- |           1 | User successfully registered |
-- +-------------+------------------------------+

-- We're gonna do that exact same call, so that we can ensure we get an message on duplicates
CALL sp_register('comp440_sabra', TRUE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @message);
SELECT @registered, @message;

-- RETURN
-- +-------------+-------------------------+
-- | @registered | @message                |
-- +-------------+-------------------------+
-- |           0 | Username already exists |
-- +-------------+-------------------------+

-- 2. (cont) Unmatching passwords should be detected, as well.

-- Drop existing procedure
DROP PROCEDURE IF EXISTS sp_login;

-- Create a procedure for user login .. This is most likely not correct, as we should be hashing and salting values
-- before they get here but whatever.. This is for practice purposes
-- Code can be called like so:
-- CALL sp_login('comp440_sabra', 'pass1234', @passConfirmed);
-- SELECT @passConfirmed;
DELIMITER $$
CREATE PROCEDURE sp_login( IN username varchar(255), IN password varchar(255), OUT passConfirmed BOOLEAN )
    BEGIN
        DECLARE uemail varchar(255) DEFAULT '';
        SET passConfirmed = FALSE;

        SELECT email INTO uemail FROM user u WHERE u.username=username AND u.password=password;
        IF uemail != '' THEN
            SET passConfirmed = TRUE;
        END IF;
    END $$
DELIMITER ;

-- Now the procedures been declared, let's try calling it but we want an error
CALL sp_login('comp440_sabra', 'pass12333', @passConfirmed);
SELECT @passConfirmed;

-- RETURN:
-- +----------------+
-- | @passConfirmed |
-- +----------------+
-- |              0 |
-- +----------------+

-- Now let's try calling it correctly.
CALL sp_login('comp440_sabra', 'pass1234', @passConfirmed);
SELECT @passConfirmed;

-- RETURN:
-- +----------------+
-- | @passConfirmed |
-- +----------------+
-- |              1 |  <- Boolean, 0/1, F/T
-- +----------------+
