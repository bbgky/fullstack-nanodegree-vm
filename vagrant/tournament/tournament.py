#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(dbname='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname={}".format(dbname))
    cur = db.cursor()
    return db, cur


def deleteMatches():
    """Remove all the match records from the database."""
    db, cur = connect()
    cur.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cur = connect()
    cur.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()
    cur.execute("select count(*) as num from players;")
    num = cur.fetchone()[0]
    db.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cur = connect()
    cur.execute("insert into players (name) values(%s);",
                (bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cur = connect()
    cur.execute('''
                    Select id, name, count(w_id) as wins,
                    count(w_id)+count(L.l_id) as total
                    From players
                    left join matches  on players.id = matches.w_id
                    left join (Select l_id From matches) AS L
                    on players.id = L.l_id
                    Group by id, name
                    Order by wins Desc;
                ''')
    standings = [(row[0], row[1], row[2], row[3]) for row in cur.fetchall()]
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cur = connect()

    cur.execute("INSERT INTO matches(w_id,l_id) VALUES (%s,%s); ",
                (winner, loser))
    db.commit()
    db.close()


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
    standings = playerStandings()
    pairs = []
    for i in range(len(standings)/2):
        pairs.append((standings[2*i][0], standings[2*i][1],
                      standings[2*i+1][0], standings[2*i+1][1]))
    return pairs
