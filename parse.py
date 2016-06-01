#!/usr/bin/env python

from lxml import etree
from collections import namedtuple
import datetime

from mlbgame.stats import PitcherStats
from stats import calculate_game_score

Outing = namedtuple('Outing', 'date pitcher')


def parse_for_starting_pitcher_outings(xml_file):
    doc = etree.parse(xml_file)
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


if __name__ == '__main__':
    pitcher_outings = parse_for_starting_pitcher_outings(
        '/home/brewerja/Downloads/baseball/xml/2015.xml')
    for outing in sorted(pitcher_outings, key=lambda x: x.date):
        print(outing.date, outing.pitcher.id,
              calculate_game_score(outing.pitcher))
