import time
import json
import datetime
import mysql.connector

# Simulation configuration shared with main
submodel_id = 1
total_players = 3

db_config = {
    'host':"127.0.0.1",
    'port':3306,
    'user': 'root',
    'password': 'my-secret-pw',
    'database': 'cosimplat'
}


def get_submodel_payload(payloads, target_submodel_id):
    """
    Extracts the 'submodel_payload' from the 'payload' section of a specific submodel_id.

    Args:
        payloads (list): A list of JSON strings.
        target_submodel_id (int): The submodel_id to filter by.

    Returns:
        list or None: The submodel_payload list if found, otherwise None.
    """
    for item in payloads:
        try:
            data = json.loads(item)
            if data.get('submodel_id') == target_submodel_id:
                return data.get('payload', {}).get('submodel_payload')
        except json.JSONDecodeError:
            print(f"Warning: Skipping invalid JSON: {item}")
            continue
    return None


def insert_payload_to_db(payload_json, submodel_id, simgame_id, sim_step):
    try:
        conn = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"DB connection error: {err}")
        return
    cursor = conn.cursor()
    try:
        query = ("INSERT INTO simcrono (payload, submodel_id, simgame_id, sim_step, modified) "
                 "VALUES (%s, %s, %s, %s, NOW())")
        cursor.execute(query, (payload_json, submodel_id, simgame_id, sim_step))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"SQL error: {err}")
    finally:
        cursor.close()
        conn.close()

def your_simulation(payloads, current_step):
    """
         In this function the use implement the simulation model which is run programmatically.

         """

    # Implement your simulation calculation using the payloads
    # print("Simulation output with payloads:", payloads)

    # Add your simulation logic here #########################################################################

    # 1. Extrapolate the information you need from the Payload

    submodel_data = get_submodel_payload(payloads, 3)
    print("Extracted submodel_payload from submodel_id 3:", submodel_data)

    # 2. Update the state of your simulation model with the information you were looking for

    # 3. Execute the model till the next step
    time.sleep(1.01)  # Delay for 1.3 seconds - just to simulate a process. Delete in real mode.
    # ########################################################################################################

    # 4. Insert Payload relative to the "next step" into MySQL database the result of your simulation.


    payload = {
        "simgame_id": 1,
        "submodel_id": submodel_id,
        "payload": {
            "submodel_status": "ONLINE",
            "subsim_state": "COMPLETED",
            "submodel_current_step": current_step,
            "submodel_payload": [
                {"item_id": "1_item1", "item_value": 10, "item_unit": "m", "item_meta": ""},
                {"item_id": "1_item2", "item_value": 20, "item_unit": "s", "item_meta": ""},
                {"item_id": "1_item3", "item_value": 5,  "item_unit": "kg", "item_meta": ""}
            ]
        },
        "state_history": "Initial state",
        "sim_step": current_step,
        "modified": datetime.datetime.now().isoformat()
    }

    payload_json = json.dumps(payload)
    insert_payload_to_db(payload_json, submodel_id, 1, current_step)
