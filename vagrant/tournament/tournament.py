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
    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("select count(*) as num from players;")
    num = cur.fetchall()[0][0]
    db.close()
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("insert into players (name) values(%s);",(bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("select T.id, T.name, T.wins, P.num_match from \
                (select id, name, count(matches.w_name) as wins from \
                players left join matches \
                on players.name = matches.w_name \
                group by name,id) as T \
                join  (select players.name as n, count(S.match_id) as num_match from \
                                players left join (select \
                                match_id,name from players,matches where \
                                name=w_name or name=l_name) as S on players.name = S.name \
                                group by players.name) as P \
                on T.name = P.n \
                order by T.wins desc;")
    standings = [(row[0],row[1],row[2],row[3]) for row in cur.fetchall()]
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = psycopg2.connect("dbname=tournament")
    cur = db.cursor()
    cur.execute("SELECT id, name from players where id = ANY(%s);",([winner,loser],))
    w_name={row[0]:str(row[1]) for row in cur.fetchall()}
    #print (w_name)
    cur.execute("INSERT INTO matches(w_name,l_name) VALUES (%s,%s); ",(w_name[winner],w_name[loser]))
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
    pairs=[]
    for i in range(len(standings)/2):
        pairs.append((standings[2*i][0],standings[2*i][1],standings[2*i+1][0],standings[2*i+1][1]))
    return pairs
