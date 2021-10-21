DROP TABLE IF EXISTS random;
CREATE TABLE random ( name varchar(255), email varchar(255));
START TRANSACTION;
INSERT INTO random (name, email) VALUES ('Sabra', 'sabra.bilodeau.352@my.csun.edu');
INSERT INTO random (name, email) VALUES ('Faizan', 'faizan.hussain.???@my.csun.edu');
INSERT INTO random (name, email) VALUES ('Shawn', 'shawn.morrison.???@my.csun.edu');
COMMIT;
