import db_connection
import psycopg2
from psycopg2 import sql

conn = db_connection.connect_postgres()
print(conn)


def get_top_five():
    query = "SELECT * FROM dr4072gl6cmha.public.highscores ORDER BY score DESC LIMIT 5"
    cursor = conn.cursor()
    result = cursor.execute(query)
    cursor.close()
    return result


def add_new_score(name, score):
    query = "INSERT INTO dr4072gl6cmha.public.highscores(name, score) VALUES (%s, %s)"
    data = (name, score)
    cursor = conn.cursor()
    result = cursor.execute(query, data)
    conn.commit()  # <- We MUST commit to reflect the inserted data
    cursor.close()
    return result


print(add_new_score('Peter', 69))
