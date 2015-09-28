#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    return c, DB


def deleteMatches():
    """Remove all the match records from the database."""

    c, DB = connect()

    c.execute('DELETE FROM matches;')
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""

    c, DB = connect()

    c.execute('TRUNCATE TABLE players CASCADE;')
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""

    c, DB = connect()

# using count to record the number of rows as num

    query = 'SELECT count(*) FROM players;'
    c.execute(query)

    rows = c.fetchall()
    DB.close()
    for row in rows:
        return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    c, DB = connect()
# cleaning the input to make sure there are no sql commands

    name = bleach.clean(name)

# Main action is the record a new player
    query = "INSERT INTO players (name) VALUES (%s);"
    param = (name,)
    c.execute(query, param)
 
# Getting the information of this player seprately

    c.execute("select * from players where name = (%s)", (name,))

    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,

    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    c, DB = connect()

    c.execute('SELECT * FROM standings;')
    rows = c.fetchall()
    DB.close()
    return rows


def reportMatch(winner, loser):

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    c, DB = connect()

    query = 'insert into matches values( %s,  %s);'
    param = (str(winner), (str(loser),))
    c.execute(query, param)

    DB.commit()
    DB.close()


def swissPairings():

    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
       A list of tuples, each of which contains (id1, name1, id2, name2)
       id1: the first player's unique id
       name1: the first player's name
       id2: the second player's unique id
       name2: the second player's name
    """

    c, DB = connect()
    c.execute('''SELECT a.id, a.name, b.id, b.name FROM standings AS a,
standings AS b where a.id > b.id AND a.wins = b.wins AND
a.matches = b.matches ORDER BY a.wins desc;''')
    rows = c.fetchall()
    DB.close()
    return rows

