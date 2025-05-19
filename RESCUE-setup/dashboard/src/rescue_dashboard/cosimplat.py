"""Methods to interact with the database."""

from contextlib import contextmanager
import mysql.connector


@contextmanager
def get_db_connection(db_config):
    conn = mysql.connector.connect(**db_config)
    try:
        yield conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            conn.close()


def fetch_data(last_timestamp, conn):
    if conn is None:
        print("Error: Connection to the database failed")
        return [], last_timestamp
    cursor = conn.cursor(dictionary=True)
    try:
        query = (
            "SELECT timestamp, payload, submodel_id, sim_step "
            "FROM simcrono "
            "WHERE simgame_id = 1 AND timestamp > %s "
            "ORDER BY timestamp ASC"
        )
        cursor.execute(query, (last_timestamp,))
        result = cursor.fetchall()
        if result:
            last_timestamp = result[-1]["timestamp"]
        return result, last_timestamp
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return [], last_timestamp
    finally:
        cursor.close()
