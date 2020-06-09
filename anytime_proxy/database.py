import sqlite3


class ProxyDatabase:
    def __init__(self):
        self.database = sqlite3.connect('anytime_proxy.db')
        self.cursor = self.database.cursor()
        self.init_table()

    def init_table(self):
        self.cursor.execute('''CREATE IF NOT EXISTS TABLE proxy
                     (
                         protocol varchar(255),
                         host varchar(255),
                         port SMALLINT,
                         anonymity TINYINT,
                         test_times SMALLINT,
                         average_latency SMALLINT,
                         validity TINYINT,
                         relay BOOLEAN
                     )''')

    def clear(self):
        self.cursor.execute('''DROP TABLE IF EXISTS proxy''')
        self.init_table()

    def commit(self):
        self.database.commit()

    def close(self):
        self.database.close()

    def add_proxy(self, proxy):
        self.cursor.execute(
            '''INSERT INTO proxy
            VALUES (?,?,?,?,?,?,?);''',
            proxy
        )

    def delete_proxy(self, proxy):
        self.cursor.execute(
            '''DELETE FROM proxy
            WHERE protocol=?, host=?, port=?;''',
            proxy[:2]
        )

    def update_proxy(self, proxy):
        self.cursor.execute(
            '''UPDATE proxy
            SET anonymity=?,test_times=?,average_latency=?,validity=?,relay=?
            WHERE protocol=?, host=?, port=?;''',
            proxy[2:] + proxy[:2]
        )

    def get_proxy(self, order_by_validity=True):
        if order_by_validity:
            self.cursor.execute('SELECT * FROM proxy ORDER BY validity')
        else:
            self.cursor.execute('SELECT * FROM proxy')
        return self.cursor.fetchone()

    def get_proxies(self, order_by_validity=True, size=-1):
        if order_by_validity:
            self.cursor.execute('SELECT * FROM proxy ORDER BY validity')
        else:
            self.cursor.execute('SELECT * FROM proxy')

        if size == -1:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size)
