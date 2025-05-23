import subprocess
import tomllib

from flask import Flask, redirect, render_template, request, url_for
from jinja2_fragments.flask import render_block

from rescue_dashboard.plot import plot_alerts, plot_loss

from .cosimplat import fetch_data, get_db_connection, reset_data

app = Flask(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


# Note: This only works when flask is run in single-threaded mode
progress = {}


def reset_progress():
    reset_data(config["database"])
    progress["done"] = False
    progress["last_timestamp"] = "1970-01-01 00:00:00"
    # Store progress of each model as a percentage
    for model_id in config["models"]:
        progress[model_id] = 0


reset_progress()


@app.get("/")
def index():
    stop_models()
    return render_template("index.html.j2", networks=config["networks"])


@app.post("/")
def post_index():
    network_id = request.form["network_id"]
    return redirect(url_for("network", network_id=network_id))


@app.get("/network/<network_id>")
def network(network_id):
    network = config["networks"].get(network_id)
    if not network:
        return "Network not found", 404
    return render_template(
        "network.html.j2",
        network=network,
        network_id=network_id,
        scenarios=config["scenarios"],
    )


@app.post("/network/<network_id>")
def post_network(network_id):
    scenario_id = request.form["scenario_id"]

    stop_models()
    reset_progress()
    start_models(network_id, scenario_id)

    return redirect(url_for("monitor", network_id=network_id, scenario_id=scenario_id))


model_pids = {}


def start_models(network_id, scenario_id):
    for model_id, model in config["models"].items():
        work_dir = model["work_dir"]
        script = model["script"].format(network=network_id, scenario=scenario_id)
        script_parts = script.split()

        out = open(f"{work_dir}/log.out", "w")
        err = open(f"{work_dir}/log.err", "w")

        model_pids[model_id] = subprocess.Popen(
            ["python"] + script_parts, stdout=out, stderr=err, cwd=work_dir
        )


def stop_models():
    for model, pid in model_pids.items():
        if pid:
            pid.terminate()
            pid.wait()
            model_pids[model] = None


def extract_loss():
    power_system_submodel_id = 1
    with get_db_connection(config["database"]) as conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
            sim_step,
            JSON_EXTRACT(payload, '$.payload.submodel_payload.power_system_load_loss' ) AS power_system_load_loss
            FROM simcrono
            WHERE submodel_id = %s
            ORDER BY sim_step ASC
            """
            cursor.execute(query, (power_system_submodel_id,))
            return cursor.fetchall()
        finally:
            cursor.close()


def extract_alert():
    incident_submodel_id = 3
    with get_db_connection(config["database"]) as conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
            sim_step,
            JSON_EXTRACT(payload, '$.payload.submodel_payload.nr_alerts' ) AS nr_alerts
            FROM simcrono
            WHERE submodel_id = %s
            ORDER BY sim_step ASC
            """
            cursor.execute(query, (incident_submodel_id,))
            return cursor.fetchall()
        finally:
            cursor.close()


@app.route("/monitor/<network_id>/scenario/<scenario_id>")
def monitor(network_id, scenario_id):
    network = config["networks"][network_id]
    scenario = config["scenarios"][scenario_id]

    total_steps = config["total_steps"]
    with get_db_connection(config["database"]) as conn:
        # Dashboard needs all timesteps for plotting
        # so we supply earliest timestamp
        result, last_timestamp = fetch_data(progress["last_timestamp"], conn)
        progress["last_timestamp"] = last_timestamp
        if result:
            model_steps = [r["sim_step"] for r in result]
            # Append is workaround for if result has single row, as min(*[2]) gives error
            model_steps.append(0)
            current_step = max(*model_steps)
            progress["done"] = (current_step + 1) >= total_steps
            for r in result:
                submodel_id = r["submodel_id"]
                # Database store model id as int while config uses str
                progress[str(submodel_id)] = int(
                    100 * (r["sim_step"] + 1) / total_steps
                )

    power_system_load_loss = plot_loss(extract_loss(), total_steps)
    alert_status = plot_alerts(extract_alert(), total_steps)

    if progress["done"]:
        stop_models()

    context = dict(
        network_id=network_id,
        network=network,
        scenario_id=scenario_id,
        scenario=scenario,
        models=config["models"],
        progress=progress,
        alert_status=alert_status,
        power_system_load_loss=power_system_load_loss,
    )
    if "hx-request" in request.headers:
        return render_block("monitor.html.j2", "content", **context)

    return render_template("monitor.html.j2", **context)
