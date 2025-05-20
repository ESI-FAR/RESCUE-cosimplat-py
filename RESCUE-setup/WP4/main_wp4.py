"""
 * Amsterdam 24-10-2024
 * Developed by Ermanno Lo Cascio, Stefan Verhoeven, Ole Mussmann (eScience Center)
 * Part of the RESCUE project.
 * © Annus Domini 2024. All rights reserved.
"""

import mysql.connector
import time
import json
import datetime
from wp4_model import your_simulation, submodel_id, total_players

# Database configuration
db_config = {
    'host':"127.0.0.1",
    'port':3306,
    'user': 'root',
    'password': 'my-secret-pw',
    'database': 'cosimplat'
}

players_progress = {}
collected_payloads = {}

total_steps = 30
steps = list(range(total_steps))

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"DB connection error: {err}")
        return None

def fetch_data(last_timestamp):
    conn = get_db_connection()
    if conn is None:
        return [], last_timestamp
    cursor = conn.cursor(dictionary=True)
    try:
        query = ("SELECT timestamp, payload, submodel_id, sim_step "
                 "FROM simcrono "
                 "WHERE simgame_id = 1 AND timestamp > %s "
                 "ORDER BY timestamp ASC")
        cursor.execute(query, (last_timestamp,))
        result = cursor.fetchall()
        if result:
            last_timestamp = result[-1]['timestamp']
        return result, last_timestamp
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return [], last_timestamp
    finally:
        cursor.close()
        conn.close()

def update_cosim_state(row, current_step):
    payload, metadata = extrapolate_data(row)
    player_id = metadata['submodel_id']
    players_progress[current_step].add(player_id)
    collected_payloads[current_step].append(payload)

def extrapolate_data(row):
    return row.get('payload'), {
        'timestamp': row.get('timestamp'),
        'submodel_id': row.get('submodel_id'),
        'sim_step': row.get('sim_step')
    }

def check_other_players(current_step):
    num_reported = len(players_progress[current_step])
    if num_reported == total_players:
        return True
    missing = set(range(1, total_players + 1)) - players_progress[current_step]
    return len(missing) == 1 and submodel_id in missing

def long_poll_with_simulation(steps):
    last_timestamp = '1970-01-01 00:00:00'
    polling_interval = 1
    current_step = 0
    global players_progress, collected_payloads
    players_progress = {step: set() for step in steps}
    collected_payloads = {step: [] for step in steps}

    while current_step < len(steps):
        result, last_timestamp = fetch_data(last_timestamp)

        if current_step == 0 and not result:
            print(f"WP4 co-simulation started at step 0 by submodel_id {submodel_id}.")
            your_simulation(collected_payloads[current_step], current_step)
            current_step += 1
            continue

        if result:
            print(f"Running WP4 simulation step: {steps[current_step]}")
            for row in result:
                update_cosim_state(row, current_step)

            if check_other_players(current_step):
                print(f"All WP4 players have shared data for step {steps[current_step]}.")
                your_simulation(collected_payloads[current_step], current_step)
                current_step += 1
            else:
                print(f"Waiting for WP4 players at step {steps[current_step]}.")

        time.sleep(polling_interval)

if __name__ == '__main__':
    print("Starting WP4 long-polling with simulation...")
    long_poll_with_simulation(steps)
