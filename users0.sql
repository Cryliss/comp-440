-- Let's drop any previously created versions of user table
DROP TABLE IF EXISTS user;

-- Create new user table
CREATE TABLE user (
    username    VARCHAR(255) NOT NULL,
    password    VARCHAR(255) NOT NULL DEFAULT 'pass1234',
    firstName   VARCHAR(255) NOT NULL,
    lastName    VARCHAR(255) NOT NULL,
    email       VARCHAR(255) NOT NULL
);

-- Add a unique constraint on the email
-- I initally thought email and username would be necesarry,
-- but if we all have 'como440 as a username it doesn't matter
ALTER TABLE user ADD CONSTRAINT unique_email UNIQUE (email);

-- Make username our primary key
ALTER TABLE user ADD PRIMARY KEY (username);

-- Drop existing procedure
DROP PROCEDURE IF EXISTS sp_register;

-- Create a procedure for user registration
-- Code can be called like so:
-- CALL sp_register('comp440', true, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @error);
-- SELECT @registered, @error;
DELIMITER $$
CREATE PROCEDURE sp_register( username VARCHAR(255), passConfirmed BOOLEAN, firstName VARCHAR(255), lastName VARCHAR(255), email VARCHAR(255), registered BOOLEAN, error VARCHAR(255))
    BEGIN
        DECLARE numrecords, numrecordsnew INT DEFAULT 0;
        DECLARE usr VARCHAR(255);

        SELECT COUNT(*) INTO numrecords FROM user;

        IF !passConfirmed THEN
            SET @registered = FALSE;
            SET @error = 'Password was not confirmed??';
        ELSE
            SELECT username INTO usr FROM user WHERE username=username;

            IF usr = username THEN
                SET @registered = FALSE;
                SET @error = 'Username already exists!';
            ELSE
                INSERT IGNORE INTO user (username, password, firstName, lastName, email) VALUES ( username, DEFAULT, firstName, lastName, email);
                SELECT COUNT(*) INTO numrecordsNew FROM user;

                IF numrecords = numrecordsNew THEN
                    SET @registered = FALSE;
                    SET @error = 'Duplicate email entry! User already registered';
                ELSE
                    SET @registered = TRUE;
                END IF;
            END IF;
        END IF;
    END $$
DELIMITER ;

-- Okay, now that the procedure is defined, let's try calling it, but we want to call
-- it saying that the password is not confirmed so we get an error.
CALL sp_register('comp440_sabra', FALSE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @error);
SELECT @registered, @error;

SET @registered = FALSE;
SET @error = NULL;

-- Let's add Shawn and Faizan to the table using a traditional transation.
START TRANSACTION;
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_faizan', 'pass1234', 'Faizan', 'Hussain', 'faizan.hussain.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_shawn', 'pass1234', 'Shawn', 'Morrison', 'shawn.morrison.???@my.csun.edu');
COMMIT;

-- Now let's try adding me again. This time it should work.
CALL sp_register('comp440_sabra', TRUE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @error);
SELECT @registered, @error;

-- We're gonna do that exact same call, so that we can ensure we get an error on duplicates
CALL sp_register('comp440_sabra', TRUE, 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu', @registered, @error);
SELECT @registered, @error;


-- Drop existing procedure
DROP PROCEDURE IF EXISTS sp_login;

-- Create a procedure for user login
-- Code can be called like so:
-- CALL sp_login('comp440_sabra', 'pass1234', @passConfirmed);
-- SELECT @passConfirmed;
DELIMITER $$
CREATE PROCEDURE sp_login( username VARCHAR(255), password VARCHAR(255), passConfirmed BOOLEAN )
    BEGIN
        DECLARE uemail VARCHAR(255);
        SET @passConfirmed = FALSE;

        SELECT email INTO uemail FROM user WHERE username = username AND password = password;
        IF uemail != NULL THEN
            SET @passConfirmed = TRUE;
        END IF;
    END $$
DELIMITER ;

-- Now the procedures been declared, let's try calling it but we want an error
CALL sp_login('comp440_sabra', 'pass12333', @passConfirmed);
SELECT @passConfirmed;

-- Now let's try calling it correctly.
CALL sp_login('comp440_sabra', 'pass1234', @passConfirmed);
SELECT @passConfirmed;
