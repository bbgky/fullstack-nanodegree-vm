-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
Drop database IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id serial PRIMARY KEY,
  name text
);

CREATE TABLE matches (
  match_id serial PRIMARY KEY,
  w_id int REFERENCES players(id),
  l_id int REFERENCES players(id)
);

CREATE VIEW standings AS
  Select id, name, count(w_id) as wins,
        count(w_id)+count(L.l_id) as total
        From players
        left join matches  on players.id = matches.w_id
        left join (Select l_id From matches) AS L
        on players.id = L.l_id
        Group by id, name
        Order by wins Desc;
