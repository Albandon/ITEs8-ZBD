import psycopg2 as pg

def get_connection():
    return pg.connect(
        database="MedicalApptApp",
        user="zbd-user",
        password="zbd-user",
        host="localhost"
    )