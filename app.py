from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = "data"
IMG_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

live_status = {
    "system_on": False,
    "stage": "Idle",
    "timestamp": None,
    "last_image": None,
    "alcohol": None
}

event_history = []

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify(live_status)

@app.route("/api/event", methods=["POST"])
def update_event():
    data = request.json
    live_status.update({
        "system_on": data.get("system_on", live_status["system_on"]),
        "stage": data.get("stage", live_status["stage"]),
        "timestamp": datetime.now().isoformat(),
        "alcohol": data.get("alcohol")
    })

    event_history.append({
        "event": live_status["stage"],
        "alcohol": live_status["alcohol"],
        "time": live_status["timestamp"],
        "image": live_status["last_image"]
    })

    return jsonify({"status": "ok"})

@app.route("/api/upload-image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    filename = f"{int(time.time())}.jpg"
    path = os.path.join(IMG_DIR, filename)
    file.save(path)

    live_status["last_image"] = filename

    return jsonify({"uploaded": filename})

@app.route("/api/events", methods=["GET"])
def get_events():
    return jsonify(event_history)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Breathalyzer API Running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
