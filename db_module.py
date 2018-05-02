import sqlite3
import os


class DBHandler:
    """

    """
    def __init__(self):
        self.database_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'astro.sqlite')

    def get_db(self):
        """
        Returns a database connection. If a connection has already been
        created, the existing connection is used, otherwise it creates a new
        connection.
        """

        try:
            sqlite_db = self.sqlite_db
        except AttributeError:
            self.sqlite_db = self.connect_db(self)

        return self.sqlite_db

    @staticmethod
    def connect_db(self):
        """
        Returns a sqlite connection object associated with the application's
        database file.
        """

        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row

        return conn

    def init_db(self):
        conn = self.get_db()

        astro_sql = '''
        DROP TABLE IF EXISTS singles;
        DROP TABLE IF EXISTS signs;
        DROP TABLE IF EXISTS genders;

        CREATE TABLE genders(id INTEGER PRIMARY KEY, name TEXT);

        CREATE TABLE signs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            start_date TEXT,
            end_date TEXT
            );

        CREATE TABLE singles(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender_id INTEGER,
            sign_id INTEGER,
            preference_id INTEGER,
            bio TEXT,
            FOREIGN KEY(sign_id) REFERENCES sign(id),
            FOREIGN KEY(gender_id) REFERENCES genders(id),
            FOREIGN KEY(preference_id) REFERENCES genders(id)
            );

        INSERT INTO genders(name) VALUES('male'), ('female'), ('non-binary');

        INSERT INTO signs(name, start_date, end_date)
            VALUES('Aquarius', 'January 20', 'February 18'),
            ('Pisces', 'February 20', 'March 20'),
            ('Aries', 'March 21', 'April 19'),
            ('Taurus', 'April 20', 'May 20'),
            ('Gemini', 'May 21', 'June 20'),
            ('Cancer', 'June 21', 'August 23'),
            ('Leo', 'July 23', 'Apr 22'),
            ('Virgo', 'August 23', 'September 22'),
            ('Libra', 'September 23', 'October 22'),
            ('Scorpio', 'October 23', 'November 21'),
            ('Sagittarius', 'November 22', 'December 21'),
            ('Capricorn', 'December 22', 'January 19');'''

        conn.cursor().executescript(astro_sql)

    def initdb_command(self):
        self.init_db()
        print('Initialized the database.')

    def get_all_users(self):
        """
        Returns all of the rows from a table as a list of dictionaries. This is
        suitable for passing to jsonify().

        :return: list of dictionaries representing the table's rows
        """

        conn = self.get_db()
        cur = conn.cursor()

        query = '''
        SELECT singles.id AS id,
        genders.name AS gender,
        signs.name AS sign,
        singles.age AS age,
        singles.name AS name,
        pref.name AS preference,
        singles.bio AS bio
        FROM singles
        INNER JOIN genders ON  genders.id = singles.gender_id
        INNER JOIN signs ON signs.id= singles.sign_id
        INNER JOIN genders AS pref ON pref.id = singles.preference_id'''

        results = []

        for row in cur.execute(query):
            results.append(dict(row))
        return results

    def get_by_id(self, uid):

        conn = self.get_db()
        cur = conn.cursor()

        query = '''
        SELECT singles.id AS id,
        genders.name AS gender,
        signs.name AS sign,
        singles.age AS age,
        singles.name AS name,
        pref.name AS preference,
        singles.bio AS bio
        FROM singles
        INNER JOIN genders ON  genders.id = singles.gender_id
        INNER JOIN signs ON signs.id= singles.sign_id
        INNER JOIN genders AS pref ON pref.id = singles.preference_id
        WHERE singles.id = ?'''

        cur.execute(query, (uid,))
        user = cur.fetchone()
        if(user == None):
            return dict()
        else:
            return(dict(user))

    def post(self, gender, sign, name, age, preference, bio):
        conn = self.get_db()
        cur = conn.cursor()

        query = """SELECT id FROM genders WHERE name = ?"""
        cur.execute(query, (gender,))
        gender_id = cur.fetchone()['id']

        query = """SELECT id FROM signs WHERE name = ?"""
        cur.execute(query, (sign,))
        sign_id = cur.fetchone()['id']

        query = """SELECT id FROM genders WHERE name = ?"""
        cur.execute(query, (preference,))
        preference_id = cur.fetchone()['id']

        query = """INSERT INTO singles(name, age, gender_id, sign_id,
        preference_id, bio) VALUES(?, ?, ?, ?, ?, ?)"""
        cur.execute(query, (name, age, gender_id, sign_id, preference_id, bio))
        conn.commit()
