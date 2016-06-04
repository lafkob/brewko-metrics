-- To load this into a sqlite database, at the prompt, run the following command:
-- .read create.sql
CREATE TABLE starts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, date DATE, postseason INTEGER, pitcher_id VARCHAR, site VARCHAR, game_score INTEGER, outs INTEGER, hits integer, runs INTEGER, earned_runs INTEGER, walks INTEGER, strikeouts INTEGER);
CREATE TABLE games (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, date DATE, postseason INTEGER, site VARCHAR, total_runs INTEGER);
.separator ,
.mode csv
.import starts.csv starts
.import games.csv games
ALTER TABLE starts ADD COLUMN park_factor DOUBLE;
