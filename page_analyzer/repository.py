import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    