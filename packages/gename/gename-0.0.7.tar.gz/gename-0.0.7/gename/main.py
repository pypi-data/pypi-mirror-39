import sqlite3
import os


here = os.path.abspath(os.path.dirname(__file__))


class Gender:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(here, 'names.db'))
        self.cur = self.conn.cursor()

    def speculate(self, name):
        self.cur.execute(
            'SELECT gender from name_gender WHERE name=?',
            (name.lower(),)
        )
        res = self.cur.fetchone()
        if res:
            return res[0]
        return 'U'
