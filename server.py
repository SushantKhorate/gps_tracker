from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = {
    "lat": None,
    "lon": None,
    "card": None
}

@app.route('/api/gps', methods=['POST'])
def receive():
    global data_store
    data_store = request.json
    print("Received:", data_store)
    return {"status": "ok"}

@app.route('/api/data')
def data():
    return jsonify(data_store)

@app.route('/')
def home():
    return "Server is running"

if __name__ == "__main__":
    app.run()
