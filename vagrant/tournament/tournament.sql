-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players(name TEXT,time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,id serial primary key);


create table matches (id SERIAL , wins smallint, losses smallint); 

create view standings as select matches.id, name, wins, wins+losses as matches from players, matches where players.id = matches.id order by wins desc and losses;
