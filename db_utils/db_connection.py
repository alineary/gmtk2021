import os
import psycopg2

import db_utils.env


USER = db_utils.env.POSTGRES_USER
PASSWORD = db_utils.env.POSTGRES_PASSWORD
HOST = db_utils.env.POSTGRES_HOST
DB = db_utils.env.POSTGRES_DB


def connect_postgres():
    try:
        return psycopg2.connect(dbname=DB, user=USER, password=PASSWORD, host=HOST)
    except psycopg2.OperationalError:
        return "CONNECTION ERROR #2269"
