#!/usr/bin/env python

import sqlite3


class ParkFactor(object):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def get_avg_runs_at_site_in_last_100_games(self, site, date):
        query = ("SELECT sum(total_runs) FROM "
                 "(SELECT total_runs FROM games "
                 " WHERE site = '{}' AND date < '{}' "
                 " ORDER BY date DESC limit 100)").format(site, date)
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0] / 100

    def games_before_date(self, site, date):
        query = ("SELECT count(*) FROM games "
                 "WHERE site = '{}' AND date < '{}'").format(site, date)
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return int(result[0])
        return 0

    def get_park_factor(self, site, date):
        if self.games_before_date(site, date) > 99:
            avg_runs = self.get_avg_runs_at_site_in_last_100_games(site, date)
            return 2 * avg_runs - 18
        return 0

    def set_park_factors(self):
        outing_cursor = self.conn.cursor()
        update_cursor = self.conn.cursor()
        outing_cursor.execute('SELECT id, site, date FROM starts')
        i = 1
        while True:
            outing = outing_cursor.fetchone()
            if not outing:
                break
            i += 1
            if i % 1000 == 0:
                self.conn.commit()
                print(i)
            id, site, date = outing
            factor = pf.get_park_factor(site, date)
            update_cursor.execute('UPDATE starts SET park_factor = {} '
                                  'where id = {}'.format(factor, id))
        self.conn.commit()

if __name__ == '__main__':
    pf = ParkFactor('starts.db')
    pf.set_park_factors()
