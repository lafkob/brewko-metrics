#!/usr/bin/env python

import sqlite3


class ParkFactor(object):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def get_site_reg_season_stats(self, site, year):
        query = ("SELECT count(*), sum(total_runs) FROM games "
                 "WHERE site = '{}' AND postseason=0 AND "
                 "strftime('%Y', date) =  '{}'").format(site, year)
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return int(result[0]), int(result[1])
        return 0

    def get_park_factor(self, site, year):
        num_games, total_runs = self.get_site_reg_season_stats(site, year)
        if num_games >= 50:
            avg_runs = total_runs / num_games
            return 2 * avg_runs - 18
        return 0

    def set_park_factors(self):
        outing_cursor = self.conn.cursor()
        update_cursor = self.conn.cursor()
        outing_cursor.execute("SELECT id, site, strftime('%Y', date) as year "
                              "FROM starts")
        i = 1
        while True:
            outing = outing_cursor.fetchone()
            if not outing:
                break
            i += 1
            if i % 100 == 0:
                self.conn.commit()
                print(i)
            id, site, year = outing
            factor = pf.get_park_factor(site, year)
            update_cursor.execute('UPDATE starts SET park_factor = {} '
                                  'where id = {}'.format(factor, id))
        self.conn.commit()

if __name__ == '__main__':
    pf = ParkFactor('starts.db')
    pf.set_park_factors()
