-- This file is for the functions we're going to define for the blogger database
-- to satify the requirements for phase 2
USE `blogger`;

-- User should insert a blog like
-- sp_insertPost( IN subject varchar(50), IN description varchar(500), IN tags []varchar(50),
--      OUT success boolean, OUT message varchar(50) )
-- CONSTRAINT: 2 blog posts per day (per user)

-- ALTER DATABASE blogger CHARACTER SET utf8 COLLATE utf8_general_ci;
DROP PROCEDURE IF EXISTS sp_insertPost;

DELIMITER $$
CREATE PROCEDURE sp_insertPost (
    IN subject varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN description varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN posted_by varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN pdate date,
    IN tags varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    OUT blogid int(10), OUT message varchar(250)
)
    BEGIN
        DECLARE tag varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
        DECLARE numPosts int(2) DEFAULT NULL;
        DECLARE bid int(10) DEFAULT NULL;
        DECLARE idx,prev_idx int;

        SET blogid = -1;


        SELECT COUNT(*) INTO numPosts FROM blogs b WHERE b.created_by=posted_by AND b.pdate=pdate;
        IF numPosts = 2 THEN
            SET message = 'You have already posted 2 blogs today, you cannot create anymore!';
        ELSE
            START TRANSACTION;
            INSERT INTO blogs ( subject, description, pdate, created_by ) VALUES ( subject, description, pdate, posted_by );
            COMMIT;

            SELECT LAST_INSERT_ID() INTO bid FROM blogs LIMIT 1;

            IF bid IS NOT NULL THEN
                SET blogid = bid;
                SET message = 'Blog successfully added to the database.';
                -- TODO: FIX THIS -- MAKES INSERT BREAK KINDA
                SET idx = LOCATE(',',tags,1);
                SET prev_idx = 1;

                WHILE idx > 0 DO
                    SET tag = SUBSTR(tags, idx, idx-prev_idx);
                    START TRANSACTION;
                    INSERT IGNORE INTO blogstags ( blogid, tag ) VALUES ( bid, tag );
                    COMMIT;
                    SET prev_idx = idx+1;
                    SET idx = LOCATE(',', tags, prev_idx);
                END WHILE;
                SET tag = SUBSTR(tags, prev_idx);
                START TRANSACTION;
                INSERT IGNORE INTO blogstags ( blogid, tag ) VALUES ( bid, tag );
                COMMIT;
            END IF;
        END IF;
    END $$
DELIMITER ;

-- User should be able to select a blog from a list
-- Should be able to make a 'negative' or 'positive' review of the post
-- with a description
-- CONSTRAINT: 3 comments per day, 1 comment per blog (per user)
--              Cannot comment on own blog

DROP PROCEDURE IF EXISTS sp_comment;

DELIMITER $$
CREATE PROCEDURE sp_comment(
    IN sentiment varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN description varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    IN cdate date,
    IN blogid int(10),
    IN poster varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    OUT commentid int(10), OUT message varchar(50)
)
    BEGIN
        DECLARE numComments int(2) DEFAULT NULL;
        DECLARE bid, cid int(10) DEFAULT NULL;
        DECLARE usr varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL;

        SET commentid = -1;

        SELECT created_by INTO usr FROM blogs b WHERE b.blogid=blogid;
        IF usr = '' THEN SET message = 'Invalid blog id somehow?';
        ELSEIF usr = poster THEN SET message = 'You cannot comment on your own blog post!';
        ELSE
            SELECT COUNT(*) INTO numComments FROM comments c WHERE c.posted_by=poster AND c.cdate=cdate;
            IF numComments = 3 THEN
                SET message = 'You cannot post more than 3 comments in a day!';
            ELSE
                SELECT commentid INTO cid FROM comments c WHERE c.posted_by=poster AND c.blogid=blogid LIMIT 1;
                IF cid IS NOT NULL THEN
                    SET message = 'You cannot comment on a blog more than once!';
                ELSE
                    START TRANSACTION;
                    INSERT INTO comments ( sentiment, description, cdate, blogid, posted_by )
                        VALUES ( sentiment, description, cdate, blogid, poster );
                    COMMIT;

                    SELECT LAST_INSERT_ID() INTO cid FROM comments LIMIT 1;
                    IF cid IS NOT NULL THEN
                        SET commentid = cid;
                        SET message = 'Comment successfully added.';
                    ELSE
                        SET message = 'Error setting comment, double check your input!';
                    END IF;
                END IF;
            END IF;
        END IF;
    END $$
DELIMITER ;
