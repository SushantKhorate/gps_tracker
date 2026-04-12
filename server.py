from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

data_store = {
    "lat": None,
    "lon": None,
    "time": None
}

@app.route('/api/gps', methods=['POST'])
def receive():
    global data_store
    data = request.json

    data_store = {
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
