-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--  Drop any databases to allow the creation of a tournament database

DROP DATABASE IF EXISTS tournament;

-- Create database tournament

CREATE DATABASE tournament;

--Connect to the database

\c tournament

-- Making the table to record players and their unique identifier keys

CREATE TABLE players(
       name TEXT,
       TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       id SERIAL PRIMARY KEY
);

--Making matches table to record the matches key with unique id key

CREATE TABLE MATCHES (
        
       winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
       loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
       id SERIAL PRIMARY KEY
       CHECK (winner <> loser)
); 

--Creating a view to list requirements of the project and give a picture of the tournament

CREATE VIEW STANDINGS AS SELECT 
       	      players.id, 
       	      name, 
       	      COUNT(CASE players.id WHEN winner THEN 1 ELSE NULL END) AS wins,
       	      COUNT(matches.id) AS matches FROM players 
       	      LEFT JOIN matches ON players.id IN (winner, loser) 
	      GROUP BY  players.id, name ORDER BY wins DESC ;