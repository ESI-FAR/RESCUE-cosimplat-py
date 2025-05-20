import subprocess
import tomllib
from pathlib import Path
from textwrap import dedent
from time import sleep

from flask import Flask, redirect, render_template, request, url_for
from jinja2_fragments.flask import render_block

from .cosimplat import fetch_data, get_db_connection

app = Flask(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Note: This only works when flask is run in single-threaded mode
progress = {
    "current_step": 0,
}


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
    progress["current_step"] = 0

    selection_file = Path("../WP2/selection.toml")
    selection_file.write_text(
        dedent(f"""\
        network = {network_id}
        scenario = {scenario_id}    
    """)
    )

    stop_models()
    start_models()

    return redirect(url_for("monitor", network_id=network_id, scenario_id=scenario_id))


model_pids = {
    "wp2": None,
    "wp3": None,
    "wp4": None,
}


def start_models():
    wp2_out = open("../WP2/log.out", "w")
    wp2_err = open("../WP2/log.err", "w")
    wp3_out = open("../WP3/log.out", "w")
    wp3_err = open("../WP3/log.err", "w")
    wp4_out = open("../WP4/log.out", "w")
    wp4_err = open("../WP4/log.err", "w")

    model_pids["wp2"] = subprocess.Popen(
        ["python", "main_wp2.py"], stdout=wp2_out, stderr=wp2_err, cwd="../WP2"
    )
    model_pids["wp3"] = subprocess.Popen(
        ["python", "main_wp3.py"], stdout=wp3_out, stderr=wp3_err, cwd="../WP3"
    )
    model_pids["wp4"] = subprocess.Popen(
        ["python", "main_wp4.py"], stdout=wp4_out, stderr=wp4_err, cwd="../WP4"
    )


def stop_models():
    for model, pid in model_pids.items():
        if pid:
            pid.terminate()
            pid.wait()
            model_pids[model] = None


@app.route("/monitor/<network_id>/scenario/<scenario_id>")
def monitor(network_id, scenario_id):
    network = config["networks"][network_id]
    scenario = config["scenarios"][scenario_id]

    with get_db_connection(config["database"]) as conn:
        # Dashboard needs all timesteps for plotting
        # so we supply earliest timestamp
        epoch = "1970-01-01 00:00:00"
        result, _ = fetch_data(epoch, conn)

    # TODO extract data from result
    sleep(0.1)  # Simulate some processing time
    progress["current_step"] += 1
    total_steps = config["total_steps"]
    alert_status = "NOMINAL"
    power_system_load_loss = 0

    if progress["current_step"] >= total_steps:
        stop_models()

    context = dict(
        network_id=network_id,
        network=network,
        scenario_id=scenario_id,
        scenario=scenario,
        current_step=progress["current_step"],
        total_steps=total_steps,
        alert_status=alert_status,
        power_system_load_loss=power_system_load_loss,
    )
    if "hx-request" in request.headers:
        return render_block("monitor.html.j2", "content", **context)

    return render_template("monitor.html.j2", **context)
