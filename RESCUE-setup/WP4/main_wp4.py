'''
 * Amsterdam 24-10-2024
 * This software has been developed by Ermanno Lo Cascio, Stefan Verhoeven and Ole Mussmann
 * of the eScience Center (ESI-FAR Team), AMSTERDAM - The Netherlands.
 * This work is part of the RESCUE project.
 * © Annus Domini 2024. All rights reserved.
 '''


import mysql.connector
import time
import json
import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password here if applicable. Not needed on localhost
    'database': 'cosimplat'
}

# Global variable to track players' progress and collected payloads
players_progress = {}
collected_payloads = {}

# Global variable for submodel_id and number of players
submodel_id = 3  # Set the desired submodel ID here. NB Submodel number 1 is by definition the Game Leader.
total_players = 3 # Set the number of players here

# Define the total number of simulation steps
total_steps = 30

# Create the list using a loop
steps = []
for i in range(total_steps):
    steps.append(i)

# Function to get the database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn  # Return the connection object if successful
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Log the error for debugging
        return None  # Return None if connection fails


# Here the MySQL database, i.e. fetch and return new rows inserted in the table simcrono
def fetch_data(last_timestamp):
    conn = get_db_connection()
    if conn is None:
        print("Error: Connection to the database failed")
        return [], last_timestamp
    cursor = conn.cursor(dictionary=True)
    try:
        # Query to fetch new data based on the last timestamp
        query = ("SELECT timestamp, payload, submodel_id, sim_step "
                 "FROM simcrono "
                 "WHERE simgame_id = 1 AND timestamp > %s "  # The game id is set to 1. Pass a variable eventually, if needed.
                 "ORDER BY timestamp ASC")
        cursor.execute(query, (last_timestamp,))
        result = cursor.fetchall()

        if result:
            # Update the last_timestamp to the latest one fetched
            last_timestamp = result[-1]['timestamp']

        return result, last_timestamp
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return [], last_timestamp
    finally:
        cursor.close()
        conn.close()


# Main long-polling loop with nested stepped simulation
def long_poll_with_simulation(steps):
    last_timestamp = '1970-01-01 00:00:00'  # Initial timestamp
    polling_interval = 1  # Time to sleep between polling attempts
    steps = steps # Set the total amount of sim steps required
    current_step = 0  # Start with the first simulation step

    # Initialize players_progress and collected_payloads for the current simulation step
    global players_progress, collected_payloads
    players_progress = {step: set() for step in steps}  # Reset for each run
    collected_payloads = {step: [] for step in steps}  # Reset for each run

    # Simulation loop
    while current_step < len(steps):
        # Poll for new data
        result, last_timestamp = fetch_data(last_timestamp)

        # Check the special condition for step 0 and submodel_id
        if current_step == 0 and submodel_id == submodel_id and not result:
            print(f"Co-simulation started at step 0 by submodel_id {submodel_id}.")
            your_simulation(collected_payloads[current_step], current_step)  # Proceed with simulation for step 0
            current_step += 1  # Move to the next step
            continue  # Skip the rest of the loop and continue to the next iteration

        if result:
            # If new data is available, process each row
            print(f"Running simulation step: {steps[current_step]}")
            for row in result:
                # Check for next-step condition and eventually go ahead with the simulation
                update_cosim_state(row, current_step)

            # Check if all players have shared their payload
            if check_other_players(current_step):
                print(f"All players have shared data for step {steps[current_step]}.")

                # Pass the collected payloads to the simulation function
                your_simulation(collected_payloads[current_step], current_step)

                # Proceed to the next simulation step
                current_step += 1
            else:
                print(f"Waiting for all players to share data for step {steps[current_step]}.")

        # Sleep between polling attempts
        time.sleep(polling_interval)



def update_cosim_state(row, current_step):
    # Extract the payload and metadata from the row
    payload, metadata = extrapolate_data(row)

    # Update the players_progress
    player_id = metadata['submodel_id']
    players_progress[current_step].add(player_id)

    # Collect the payload for the current step
    collected_payloads[current_step].append(payload)


def check_other_players(current_step):
    """
    Check whether all the players have reached the current step. If the only missing player
    is the one running the simulation (current_submodel_id), proceed without waiting.
    """
    # Number of players who have reported their data for this step
    num_players_reported = len(players_progress[current_step])

    # If all players have reported, we can proceed
    if num_players_reported == total_players:
        return True

    # If only one player is missing, check if it's the current player (submodel_id)
    missing_players = set(range(1, total_players + 1)) - players_progress[current_step]
    if len(missing_players) == 1 and submodel_id in missing_players:
        # The current player is the missing one, proceed with the simulation
        return True

    return False


# Function to extrapolate payload and metadata from a database row
def extrapolate_data(row):
    # Extract the payload
    payload = row.get('payload')

    # Extract metadata
    metadata = {
        'timestamp': row.get('timestamp'),
        'submodel_id': row.get('submodel_id'),
        'sim_step': row.get('sim_step')
    }

    # Return both the payload and metadata for further processing
    return payload, metadata


def your_simulation(payloads, current_step):
    """
       In this function the use implement the simulation model which is run programmatically.

       """

    # Implement your simulation calculation using the payloads
    #print("Simulation output with payloads:", payloads)

    # Add your simulation logic here #########################################################################

    # 1. Extrapolate the information you need from the Payload

    # 2. Update the state of your simulation model with the information you were looking for

    # 3. Execute the model till the next step
    time.sleep(1.01)  # Delay for 1.3 seconds - just to simulate a process. Delete in real mode.
    # ########################################################################################################

    # 4. Insert Payload relative to the "next step" into MySQL database the result of your simulation.

    current_timestamp_in_seconds = int(time.time())  # Current timestamp in seconds
    submodel_status = "ONLINE" # Eventually needed to handle special scenarios
    subsim_state = "COMPLETED" # Eventually needed to handle special scenarios
    submodel_current_step = current_step   # simulated step of the model
    simgame_id = 1 # Change with appropriate game id

    # Construct the payload template
    payload = {
        "simgame_id": simgame_id,
        "submodel_id": submodel_id,
        "payload": {
            "submodel_status": submodel_status,
            "subsim_state": subsim_state,
            "submodel_current_step": submodel_current_step,
            "submodel_payload": [
                {"item_id": "1_item1", "item_value": 10, "item_unit": "m", "item_meta": ""},  #customize it
                {"item_id": "1_item2", "item_value": 20, "item_unit": "s", "item_meta": ""},  #customize it
                {"item_id": "1_item3", "item_value": 5, "item_unit": "kg", "item_meta": ""}   #customize it
            ]
        },
        "state_history": "Initial state",  # Eventually needed to handle special scenarios
        "sim_step": submodel_current_step,
        "modified": datetime.datetime.now().isoformat()  # Current timestamp in ISO format
    }

    # Convert the payload to a JSON string for database storage
    payload_json = json.dumps(payload)

    # Insert the constructed payload into the MySQL database
    insert_payload_to_db(payload_json, submodel_id, simgame_id, submodel_current_step)

    return


def insert_payload_to_db(payload_json, submodel_id, simgame_id, sim_step):
    conn = get_db_connection()  # Reuse your existing function to get DB connection
    if conn is None:
        print("Error: Connection to the database failed")
        return

    cursor = conn.cursor()
    try:
        # SQL statement to insert the payload into the database
        insert_query = ("INSERT INTO simcrono (payload, submodel_id, simgame_id, sim_step, modified) "
                        "VALUES (%s, %s, %s, %s, NOW())")
        cursor.execute(insert_query, (payload_json, submodel_id, simgame_id, sim_step))
        conn.commit()  # Commit the transaction

        #print("Payload inserted successfully.")
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
    finally:
        cursor.close()
        conn.close()


# Start the long-polling with simulation
if __name__ == '__main__':
    print("Starting long-polling with simulation...")
    long_poll_with_simulation(steps)


