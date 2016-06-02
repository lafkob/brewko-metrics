#!/usr/bin/env python

import os
import itertools
import csv
from lxml import etree
from collections import namedtuple
import datetime

from mlbgame.stats import PitcherStats

Outing = namedtuple('Outing', 'date pitcher site')


def parse_for_starting_pitcher_outings(xml_file):
    with open(xml_file) as f:
        it = itertools.chain('<games>', f, '</games>')
        doc = etree.fromstringlist(it)
        pitcher_outings = []
        for boxscore in doc.findall('boxscore'):
            year, month, day = map(lambda x: int(x),
                                   boxscore.get('date').split('/'))
            date = datetime.date(year, month, day)
            site = boxscore.get('site')
            for pitching in boxscore.findall('pitching'):
                for pitcher in pitching.findall('pitcher'):
                    p = PitcherStats(pitcher.attrib)
                    p.out = p.outs  # slight difference
                    if p.gs == 1:
                        pitcher_outings.append(Outing(date, p, site))
                        break
    return pitcher_outings


def innings_completed_past_the_fourth(outs):
    return max(outs - 4 * 3, 0) // 3


def calculate_game_score(player):
    return (50 + player.out +
            2 * innings_completed_past_the_fourth(player.out) +
            player.so - 2 * player.h - 4 * player.er -
            2 * (player.r - player.er) - player.bb)


def parse_all(path):
    for file in os.listdir(path):
        if int(file.split('.')[0]) > 1959:
            print(path + '/' + file)
            yield parse_for_starting_pitcher_outings('%s/%s' % (path, file))


def write_all(path, writer):
    for outings in parse_all(path):
        for outing in outings:
            p = outing.pitcher
            writer.writerow([outing.date, p.id, outing.site,
                             calculate_game_score(p),
                             p.out, p.h, p.r, p.er, p.bb, p.so])


if __name__ == '__main__':
    paths = ['regular_season/box_scores',
             'postseason/box_scores']

    with open('starts.csv', 'w') as csvfile:
        starts_writer = csv.writer(csvfile, delimiter=',')
        for path in paths:
            write_all(path, starts_writer)
