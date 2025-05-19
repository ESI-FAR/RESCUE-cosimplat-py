import time
import json
import datetime
import mysql.connector

# Simulation configuration shared with main
submodel_id = 1
total_players = 3

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cosimplat'
}

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
    time.sleep(1.01)  # Simulate model processing time

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
