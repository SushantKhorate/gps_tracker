from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz

app = Flask(__name__)
IST = pytz.timezone('Asia/Kolkata')

events = []
relay_status = "OFF"

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

@app.route('/api/data')
def data():
    return jsonify({
        "relay": relay_status,
        "events": events
    })

@app.route('/api/off', methods=['POST'])
def off():
    global relay_status
    relay_status = "OFF"
    return {"status": "off"}

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
