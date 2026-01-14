import os
import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    #TODO: write agnostic db logic here
