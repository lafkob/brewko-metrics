#!/usr/bin/env python

import os
import itertools
import csv
from lxml import etree
from collections import namedtuple
import datetime

from mlbgame.stats import PitcherStats
from stats import calculate_game_score

Outing = namedtuple('Outing', 'date pitcher')


def parse_for_starting_pitcher_outings(xml_file):
    with open(xml_file) as f:
        it = itertools.chain('<games>', f, '</games>')
        doc = etree.fromstringlist(it)
        #doc = etree.parse(xml_file)
        pitcher_outings = []
        for boxscore in doc.findall('boxscore'):
            year, month, day = map(lambda x: int(x),
                                   boxscore.get('date').split('/'))
            date = datetime.date(year, month, day)
            for pitching in boxscore.findall('pitching'):
                for pitcher in pitching.findall('pitcher'):
                    p = PitcherStats(pitcher.attrib)
                    p.out = p.outs  # slight difference
                    if p.gs == 1:
                        pitcher_outings.append(Outing(date, p))
                        break
    return pitcher_outings


def parse_all(path):
    outings = []
    for file in os.listdir(path):
        if int(file.split('.')[0]) > 1959:
            print(path + '/' + file)
            outings.extend(
                parse_for_starting_pitcher_outings('%s/%s' % (path, file)))
    return outings


def write_all(writer, outings):
    for outing in outings:
        writer.writerow([outing.date, outing.pitcher.id,
                         calculate_game_score(outing.pitcher)])

if __name__ == '__main__':
    paths = ['regular_season/box_scores',
             'postseason/box_scores']

    with open('starts.csv', 'w') as csvfile:
        starts_writer = csv.writer(csvfile, delimiter=',')
        for path in paths:
            write_all(starts_writer, parse_all(path))
