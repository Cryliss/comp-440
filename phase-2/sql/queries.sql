-- This file is for the functions we"re going to define for the blogger database
-- to satify the requirements for phase 3
USE `blogger`;

-- 1. List all the blogs of user X, such that all the comments are positive for these blogs
SELECT * FROM blogs b WHERE b.created_by="batman" AND EXISTS (SELECT * FROM comments c WHERE b.blogid=c.blogid AND c.sentiment="positive" );

-- 2. List all the users who posted the most number of blogs on 10/10/2021; if there is a tie, list all those have a tie
SELECT DISTINCT created_by FROM blogs WHERE pdate IN (SELECT pdate FROM blogs WHERE pdate="2020-03-24");

-- 3. List users who are followed by both X and Y, where X & Y are usernames provided by the user
SELECT DISTINCT leadername FROM follows WHERE followername="catlover" AND EXISTS (SELECT leadername FROM follows WHERE followername="scooby");

-- 4. Display all users who have never posted a blog
SELECT DISTINCT username FROM user u WHERE NOT EXISTS (SELECT * FROM blogs WHERE created_by=u.username );

-- 5. Display all user who have only posted negative comments
SELECT DISTINCT posted_by FROM comments c WHERE sentiment="negative" AND NOT EXISTS (SELECT DISTINCT posted_by FROM comments c2 WHERE c2.sentiment="positive" AND c2.posted_by=c.posted_by);

-- 6. Display all users who have never received a negative comment
SELECT DISTINCT created_by FROM blogs WHERE NOT EXISTS(SELECT DISTINCT sentiment FROM comments WHERE comments.sentiment='negative' AND comments.blogid=blogs.blogid);
