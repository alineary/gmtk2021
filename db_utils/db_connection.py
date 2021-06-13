import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB = os.environ.get('POSTGRES_DB')


def connect_postgres():
    return psycopg2.connect(dbname=DB, user=USER, password=PASSWORD, host=HOST)
