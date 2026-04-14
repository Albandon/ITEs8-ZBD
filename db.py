import psycopg2 as pg

def get_connection():
    return pg.connect(
        user="postgres",
        password="postgres",
        host="localhost"
    )