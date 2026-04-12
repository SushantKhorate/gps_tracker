from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

# Indian timezone
IST = pytz.timezone('Asia/Kolkata')

data_store = {
    "lat": None,
    "lon": None,
    "time": None
}

@app.route('/api/gps', methods=['POST'])
def receive():
    global data_store
    data = request.json

    now = datetime.now(IST)

    data_store = {
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "time": now.strftime("%d-%m-%Y %I:%M:%S %p")  # 🔥 12hr format
    }

    print("Received:", data_store)
    return {"status": "ok"}

@app.route('/api/data')
def data():
    return jsonify(data_store)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
