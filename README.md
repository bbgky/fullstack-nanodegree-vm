Relational database project - swiss-system tournament
=============
Author: He Meng

python code and sql queries are located at `./vagrant/tournament`

To run the results:
1. `psql`
2. `\i tournament.sql`
3. `\q`

The first three steps are to create database and tables.

Run  `python tournament_test.py`

If the code is correct, should see output:
```
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
```
