#!/usr/bin/env python

import mlbgame


def innings_completed_past_the_fourth(outs):
    return max(outs - 4 * 3, 0) // 3


def calculate_game_score(player):
    return (50 + player.out +
            2 * innings_completed_past_the_fourth(player.out) +
            player.so - 2 * player.h - 4 * player.er -
            2 * (player.r - player.er) - player.bb)


def get_daily_starting_pitcher_stats(year, month, day):
    pitching_stats = []
    for game in mlbgame.games(year, month, day)[0]:
        try:
            game_stats = mlbgame.player_stats(game.game_id)
            pitching_stats.append(game_stats['home_pitching'][0])
            pitching_stats.append(game_stats['away_pitching'][0])
        except ValueError:
            pass  # Game doesn't exist, probably hasn't started yet
    return pitching_stats


def get_daily_starting_pitchers_by_game_score(year, month, day):
    # Some days don't have game score already calculated EX: 2009/7/1
    starting_pitchers = get_daily_starting_pitcher_stats(2016, 5, 31)
    for player in starting_pitchers:
        if not hasattr(player, 'game_score'):
            player.game_score = calculate_game_score(player)

    return sorted(starting_pitchers, key=lambda p: p.game_score, reverse=True)


def update_pitcher_rating(pitcher_score, game_score, days_since_last_start):
    return (pitcher_score * 0.97 + game_score * 0.30 -
            0.25 * (days_since_last_start - 7))


if __name__ == '__main__':
    for player in get_daily_starting_pitchers_by_game_score(2016, 5, 31):
        print(player.id, player.name_display_first_last, player.game_score)
