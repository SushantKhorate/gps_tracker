from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz

app = Flask(__name__)
IST = pytz.timezone('Asia/Kolkata')

events = []
relay_status = "OFF"
relay_command = "NONE"

gps_data = {
    "lat": None,
    "lon": None,
    "time": None
}

# -------- GPS FROM PHONE --------
@app.route('/api/gps', methods=['POST'])
def gps():
    global gps_data

    data = request.json
    now = datetime.now(IST).strftime("%d-%m-%Y %I:%M:%S %p")

    gps_data = {
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "time": now
    }

    return {"status": "ok"}


# -------- RFID EVENT --------
@app.route('/api/event', methods=['POST'])
def event():
    global relay_status

    data = request.json
    now = datetime.now(IST).strftime("%d-%m-%Y %I:%M:%S %p")

    entry = {
        "card": data.get("card"),
        "time": now,
        "relay": data.get("relay")
    }

    relay_status = entry["relay"]

    events.insert(0, entry)

    if len(events) > 20:
        events.pop()

    return {"status": "ok"}


# -------- WEB DATA --------
@app.route('/api/data')
def data():
    global relay_command

    response = {
        "relay": relay_status,
        "events": events,
        "gps": gps_data,
        "command": relay_command
    }

    relay_command = "NONE"

    return jsonify(response)


# -------- TURN OFF RELAY --------
@app.route('/api/off', methods=['POST'])
def off():
    global relay_command
    relay_command = "OFF"
    return {"status": "ok"}


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
