-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
\c tournament;
DROP table if exists players;
CREATE TABLE players (id serial, name text);
DROP table if exists matches;
CREATE TABLE matches (match_id serial, w_name text, l_name text);
