DROP TABLE IF EXISTS user;
CREATE TABLE user ( username varchar(255) NOT NULL, password varchar(255) NOT NULL, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, email varchar(255) NOT NULL);
ALTER TABLE user ADD CONSTRAINT unique_email UNIQUE (email);
ALTER TABLE user ADD PRIMARY KEY (username);
START TRANSACTION;
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_faizan', 'pass1234', 'Faizan', 'Hussain', 'faizan.hussain.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_shawn', 'pass1234', 'Shawn', 'Morrison', 'shawn.morrison.???@my.csun.edu');
INSERT INTO user (username, password, firstName, lastName, email) VALUES ('comp440_sabra', 'pass1234', 'Sabra', 'Bilodeau', 'sabra.bilodeau.352@my.csun.edu');
COMMIT;
