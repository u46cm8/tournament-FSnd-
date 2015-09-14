#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute('delete from matches;')
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""

    DB = connect()
    c = DB.cursor()
    c.execute('delete from players;')
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()

# using count to record the number of rows as num

    c.execute('select count(*) as num from players;')
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
    DB = connect()
    c = DB.cursor()

# cleaning the input to make sure there are no sql commands

    name = bleach.clean(name)

# Main action is the record a new player

    c.execute("INSERT into players values (%s)", (name,))

# Getting the information of this player seprately

    c.execute("select * from players where name = (%s)", (name,))
    row = c.fetchall()
    f_key = (row[0])[-1]

# making a record of player matches which is nessecary to make a complete entry

    c.execute("Insert into matches values (%s,0,0)", (f_key,))

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

    DB = connect()
    c = DB.cursor()
    c.execute('select * from standings;')
    rows = c.fetchall()
    DB.close()
    return rows


def reportMatch(winner, loser):

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB = connect()
    c = DB.cursor()
    c.execute('update matches set wins = wins+1 where id = %s;',
              (str(winner),))
    c.execute('update matches set losses = losses+1 where id = %s;',
              (str(loser),))
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

    DB = connect()
    c = DB.cursor()
    c.execute('''select a.id, a.name, b.id, b.name from standings as a,
standings as b where a.id > b.id and a.wins = b.wins and
a.matches = b.matches order by a.wins desc;''')
    rows = c.fetchall()
    DB.close()
    return rows

