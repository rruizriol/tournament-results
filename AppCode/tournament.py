#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()        
    cursor = DB.cursor()
    
    cursor.execute("DELETE FROM match_players")
    cursor.execute("DELETE FROM matches")
    
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()        
    cursor = DB.cursor()
    
    cursor.execute("DELETE FROM players")
    
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()        
    cursor = DB.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM players")    
    number_players = cursor.fetchone()[0]
    
    DB.close()
    
    return number_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()        
    cursor = DB.cursor()
    
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    
    DB.commit()
    DB.close()


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
    DB = connect()        
    cursor = DB.cursor()

    cursor.execute("SELECT id, name, wins, matches FROM player_standings ORDER BY wins DESC")
    player_standings = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
    
    DB.close()
    
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()        
    cursor = DB.cursor()
    
    sql_match = "INSERT INTO matches(winner) VALUES(%s) RETURNING id"
    sql_match_player = "INSERT INTO match_players (match_id,player_id,score) VALUES (%s,%s,%s)"
    
    cursor.execute(sql_match, (winner,))
    match_id = cursor.fetchone()[0]
    
    cursor.execute(sql_match_player, (match_id,winner,1))    
    cursor.execute(sql_match_player, (match_id,loser,0))
    
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
    swiss_pairings = []
    player_standings = playerStandings()
    
    for player1,player2 in zip(player_standings[0::2], player_standings[1::2]):
        swiss_pairings.append((player1[0], player1[1], player2[0], player2[1]))
    
    return swiss_pairings

