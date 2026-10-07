from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/gps', methods=['POST'])
def receive_gps():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON payload"}), 400
    
    lat = data.get("latitude")
    lon = data.get("longitude")
    speed = data.get("speed", 0)
    
    print(f"Received Telemetry -> Lat: {lat}, Lon: {lon}, Speed: {speed}")
    
    # Save to your database or store in memory for templates/index.html
    return jsonify({"status": "success", "lat": lat, "lon": lon}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
