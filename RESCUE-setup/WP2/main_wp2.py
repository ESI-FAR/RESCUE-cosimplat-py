"""
 * Amsterdam 24-10-2024
 * This software has been developed by Ermanno Lo Cascio, Stefan Verhoeven and Ole Mussmann
 * of the eScience Center (ESI-FAR Team), AMSTERDAM - The Netherlands.
 * This work is part of the RESCUE project.
 * © Annus Domini 2024. All rights reserved.
"""

import mysql.connector
import time
import json
import datetime
from wp2_model import your_simulation, submodel_id, total_players  # <-- use shared constants

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cosimplat'
}

# Global variable to track players' progress and collected payloads
players_progress = {}
collected_payloads = {}

# Define the total number of simulation steps
total_steps = 30
steps = list(range(total_steps))

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_data(last_timestamp):
    conn = get_db_connection()
    if conn is None:
        print("Error: Connection to the database failed")
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
    payload = row.get('payload')
    metadata = {
        'timestamp': row.get('timestamp'),
        'submodel_id': row.get('submodel_id'),
        'sim_step': row.get('sim_step')
    }
    return payload, metadata

def check_other_players(current_step):
    num_players_reported = len(players_progress[current_step])
    if num_players_reported == total_players:
        return True
    missing_players = set(range(1, total_players + 1)) - players_progress[current_step]
    if len(missing_players) == 1 and submodel_id in missing_players:
        return True
    return False

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
            print(f"Co-simulation started at step 0 by submodel_id {submodel_id}.")
            your_simulation(collected_payloads[current_step], current_step)
            current_step += 1
            continue

        if result:
            print(f"Running simulation step: {steps[current_step]}")
            for row in result:
                update_cosim_state(row, current_step)

            if check_other_players(current_step):
                print(f"All players have shared data for step {steps[current_step]}.")
                your_simulation(collected_payloads[current_step], current_step)
                current_step += 1
            else:
                print(f"Waiting for all players to share data for step {steps[current_step]}.")

        time.sleep(polling_interval)

if __name__ == '__main__':
    print("Starting long-polling with simulation...")
    long_poll_with_simulation(steps)
