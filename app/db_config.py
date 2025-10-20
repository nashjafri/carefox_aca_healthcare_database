import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(
        dbname="carefox_db",
        user="postgres",
        password="boxer166",
        host="localhost",
        port="5432"
    )
    conn.cursor().execute("SET search_path TO aca_individual_marketplace;")
    return conn
