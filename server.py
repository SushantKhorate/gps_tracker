from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
IST = pytz.timezone('Asia/Kolkata')

gps_data = {"lat": None, "lon": None}
gps_history = []

logs = []
counter = 1

relay_status = "OFF"
command = "NONE"

# -------- GPS --------
@app.route('/api/gps', methods=['POST'])
def gps():
    global gps_data, gps_history

    data = request.json
    now = datetime.now(IST)

    gps_data = {"lat": data["lat"], "lon": data["lon"]}

    # store hourly
    if not gps_history or (now - gps_history[0]["time"]).seconds > 3600:
        gps_history.insert(0, {
            "lat": data["lat"],
            "lon": data["lon"],
            "time": now
        })

    # keep only 1 day
    gps_history[:] = [
        x for x in gps_history
        if now - x["time"] <= timedelta(days=1)
    ]

    return {"ok": True}

# -------- SINGLE EVENT (fallback) --------
@app.route('/api/event', methods=['POST'])
def event():
    global counter, relay_status

    data = request.json
    now = datetime.now(IST)

    logs.insert(0, {
        "id": counter,
        "user": data["user"],
        "on": now.strftime("%H:%M"),
        "off": "",
        "date": now.strftime("%d-%m-%Y")
    })

    counter += 1

    if len(logs) > 30:
        logs.pop()

    relay_status = "ON"
    return {"ok": True}

# -------- BATCH EVENTS --------
@app.route('/api/event_batch', methods=['POST'])
def batch():
    global logs, counter, relay_status

    data = request.json
    now = datetime.now(IST)

    for user in data["logs"]:
        logs.insert(0, {
            "id": counter,
            "user": user,
            "on": now.strftime("%H:%M"),
            "off": "",
            "date": now.strftime("%d-%m-%Y")
        })
        counter += 1

    if len(logs) > 30:
        logs[:] = logs[:30]

    relay_status = "ON"
    return {"ok": True}

# -------- DATA --------
@app.route('/api/data')
def data():
    global command

    res = {
        "gps": gps_data,
        "logs": logs,
        "relay": relay_status,
        "command": command
    }

    command = "NONE"
    return jsonify(res)

# -------- HISTORY --------
@app.route('/api/history')
def history():
    return jsonify(gps_history)

# -------- OFF --------
@app.route('/api/off', methods=['POST'])
def off():
    global command, relay_status

    command = "OFF"
    relay_status = "OFF"

    now = datetime.now(IST).strftime("%H:%M")

    if logs:
        logs[0]["off"] = now

    return {"ok": True}

@app.route('/')
def home():
    return render_template("index.html")

app.run(host="0.0.0.0", port=5000)
