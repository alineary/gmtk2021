from db_utils import db_connection

conn = db_connection.connect_postgres()
print(conn)


def get_top_five():
    if conn == "CONNECTION ERROR #2269":
        result = [("Unable to get data", 0)]
    else:
        query = "SELECT * FROM dr4072gl6cmha.public.highscores ORDER BY score DESC LIMIT 5"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
    return result


def add_new_score(name, score):
    if conn == "CONNECTION ERROR #2269":
        return
    else:
        query = "INSERT INTO dr4072gl6cmha.public.highscores(name, score) VALUES (%s, %s)"
        data = (name, score)
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()  # <- We MUST commit to reflect the inserted data
        cursor.close()