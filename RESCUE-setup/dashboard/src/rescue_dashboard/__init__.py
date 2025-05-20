import subprocess
import tomllib
from pathlib import Path
from textwrap import dedent

from flask import Flask, redirect, render_template, request, url_for
from jinja2_fragments.flask import render_block

from .cosimplat import fetch_data, get_db_connection, reset_data

app = Flask(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def reset_progress():
    reset_data(config["database"])
    # Store progress of each model as a percentage
    model_progress = {model_id: 0 for model_id in config["models"]}
    return {
        "done": False,
        "last_timestamp": "1970-01-01 00:00:00",
    } | model_progress


# Note: This only works when flask is run in single-threaded mode
progress = reset_progress()


@app.get("/")
def index():
    stop_models()
    reset_progress()
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

    # TODO use file in ../WP2/wp2_model.py, or pass selection as argument to popen
    selection_file = Path("../WP2/selection.toml")
    selection_file.write_text(
        dedent(f"""\
        network = {network_id}
        scenario = {scenario_id}    
    """)
    )

    stop_models()
    reset_progress()
    start_models()

    return redirect(url_for("monitor", network_id=network_id, scenario_id=scenario_id))


model_pids = {}


def start_models():
    for model_id, model in config["models"].items():
        name = model["name"]
        model_dir = f"../{name.upper()}"
        out = open(f"{model_dir}/log.out", "w")
        err = open(f"{model_dir}/log.err", "w")

        script = f"main_{name}.py"
        model_pids[model_id] = subprocess.Popen(
            ["python", script], stdout=out, stderr=err, cwd=model_dir
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

    # TODO extract payloads from result
    alert_status = "NOMINAL"
    power_system_load_loss = 0

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
