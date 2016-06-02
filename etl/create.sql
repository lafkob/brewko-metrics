-- To load this into a sqlite database, at the prompt, run the following command:
-- .read create.sql
CREATE TABLE starts (date date, pitcher_id text, site text, game_score int, outs int, hits int, runs int, earned_runs int, walks int, strikeouts int);
.separator ,
.mode csv
.import starts.csv starts
