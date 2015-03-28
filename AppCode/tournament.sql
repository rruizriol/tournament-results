-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop Dabase If exists
DROP DATABASE IF EXISTS tournament;

-- Create Database
CREATE DATABASE tournament;

-- Connect to the database
\c tournament

--Create Tables
CREATE TABLE players (
    id        serial CONSTRAINT players_key PRIMARY KEY,
    name      varchar(50) NOT NULL DEFAULT ''
);

CREATE TABLE matches(
    id        serial CONSTRAINT matches_key PRIMARY KEY,
    winner    integer NOT NULL DEFAULT 0
);

CREATE TABLE match_players (
    id        serial CONSTRAINT match_players_key PRIMARY KEY,
    match_id   integer REFERENCES matches(id) NOT NULL DEFAULT 0,
    player_id  integer  REFERENCES players(id) NOT NULL DEFAULT 0,
    score     real  NOT NULL DEFAULT 0
);

--Create Views
CREATE VIEW player_standings AS 
  SELECT id
        ,name
        ,(select count(id) from matches where winner = players.id) as wins
        ,(select count(id) from match_players where player_id = players.id) as matches
        FROM players;







