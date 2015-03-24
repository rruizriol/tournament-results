# tournament-results
The Tournament Results project consists of a database schema to store the game matches between
players. Also there is a Python module to rank the players and pair them up in matches in a 
ournament.

The application files are located inside the folder AppCode. In order to execute the application do the following
- Download the repository
- Open a command console
- Change your current directory to the folder <i><b>tournament-results-database/AppCode</b></i>
- Execute the command <i><b>psql</b></i>
- Inside Postgre execute the following commands in order to create the database
    1. <i><b>CREATE DATABASE tournament;</b></i>
    2. <i><b>\i tournamen.sql</b></i>
    3. <i><b>\q</b></i>
- Execute this command <i><b>python tournament_test.py</b></i> in order to test the code
