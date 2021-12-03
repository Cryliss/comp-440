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
USE `blogger`;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = @saved_cs_client;

DROP TABLE IF EXISTS user;

-- Create new user table
CREATE TABLE user (
    `username` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `password` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `firstName` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `lastName` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`username`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Add a unique constraint on the email
-- I initally thought email and username would be necesarry,
-- but if we all have 'comp440' as a username it doesn't matter
ALTER TABLE user ADD CONSTRAINT unique_email UNIQUE (email);


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
CREATE PROCEDURE sp_register(
    IN username varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN password varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN passConfirmed boolean,
    IN firstName varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN lastName varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN email varchar(45),
    OUT registered boolean, OUT message varchar(255)
)
BEGIN
    DECLARE usr varchar(45) DEFAULT '';
    DECLARE eml varchar(100) DEFAULT '';
    SET registered = FALSE;
    SET message = '';

    -- Has the password been confirmed?
    IF !passConfirmed THEN
        SET registered = FALSE;
        SET message = 'Password was not confirmed??';
    ELSE
        -- Let's make sure we don't already have a user with this username
        SELECT username INTO usr FROM user u WHERE u.username=username LIMIT 1;
        IF usr IS NOT NULL THEN
            -- Apparently we do .. lets set our out variables
            SET registered = FALSE;
            SET message = 'Username already exists!';
        ELSE
            -- We do not! Do we already have a user with this email?
            SELECT email INTO eml FROM user u WHERE u.username=username LIMIT 1;
            IF eml IS NOT NULL THEN
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
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('faizan', 'pass1234', 'Faizan', 'Hussain', 'faizan.hussain.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('shawn', 'pass1234', 'Shawn', 'Morrison', 'shawn.morrison.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('sabra', 'pass1234', 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('batman','1234','bat','bat','nananana@batman.com'),('bob','12345','bob','bob','bobthatsme@yahoo.com'),('catlover','abcd','cat','cat','catlover@whiskers.com'),('doglover','efds','dog','dog','doglover@bark.net'),('jdoe','25478','joe','jod','jane@doe.com'),('jsmith','1111','john','smith','jsmith@gmail.com'),('matty','2222','mat','mat','matty@csun.edu'),('notbob','5555','not','bob','stopcallingmebob@yahoo.com'),('pacman','9999','pacman','pacman','pacman@gmail.com'),('scooby','8888','scoby','scoby','scooby@doo.net');
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
CREATE PROCEDURE sp_login(
    IN username varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN password varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    OUT userConfirmed BOOLEAN, OUT passConfirmed BOOLEAN
)
    BEGIN
        DECLARE pass varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '';
        DECLARE us varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '';
        SET passConfirmed = FALSE;
        SET userConfirmed = FALSE;

        SELECT password INTO pass FROM user u WHERE u.username=username AND u.password = password;
        IF pass IS NOT NULL THEN
            SET userConfirmed = TRUE;
            IF pass = password THEN
                SET passConfirmed = TRUE;
            END IF;
        END IF;
    END $$
DELIMITER ;
