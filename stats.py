#!/usr/bin/env python

import mlbgame


def get_daily_starting_pitcher_stats(year, month, day):
    pitching_stats = []
    for game in mlbgame.games(year, month, day)[0]:
        game_stats = mlbgame.player_stats(game.game_id)
        pitching_stats.append(game_stats['home_pitching'][0])
        pitching_stats.append(game_stats['away_pitching'][0])
    return pitching_stats


if __name__ == '__main__':
    for player in get_daily_starting_pitcher_stats(2012, 5, 1):
        print(player.id, player.nice_output())
