import tomllib

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


@app.get("/")
def index():
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
    # TODO Trigger simulation start
    return redirect(url_for("monitor", network_id=network_id, scenario_id=scenario_id))


@app.route("/monitor/<network_id>/scenario/<scenario_id>")
def monitor(network_id, scenario_id):
    network = config["networks"][network_id]

    # TODO update page when db changes
    current_step = 0
    total_steps = config["total_steps"]
    alert_status = "NOMINAL"
    power_system_load_loss = 0

    return render_template(
        "monitor.html.j2",
        network_id=network_id,
        scenario_id=scenario_id,
        network=network,
        current_step=current_step,
        total_steps=total_steps,
        alert_status=alert_status,
        power_system_load_loss=power_system_load_loss,
    )
