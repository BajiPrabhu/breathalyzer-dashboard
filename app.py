from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

# Folder to store uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store latest status in memory (simple storage)
status_data = {
    "status": "Idle",
    "timestamp": "",
    "last_image": ""
}


# -------------------------------
# 1) HOME ROUTE
# -------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Breathalyzer API Running"})


# -------------------------------
# 2) GET STATUS
# -------------------------------
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status_data)


# -------------------------------
# 3) UPDATE STATUS
# -------------------------------
@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json

    status_data["status"] = data.get("status", status_data["status"])
    status_data["timestamp"] = data.get("timestamp", status_data["timestamp"])
    status_data["last_image"] = data.get("last_image", status_data["last_image"])

    return jsonify({"message": "Status updated", "status": status_data})


# -------------------------------
# 4) IMAGE UPLOAD
# -------------------------------
@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file sent"}), 400

    image = request.files["image"]
    filename = f"img_{int(time.time())}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    image.save(filepath)

    file_url = f"https://breathalyzer-api.onrender.com/uploads/{filename}"

    # Store latest uploaded image in memory
    status_data["last_image"] = file_url
    status_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "message": "Image uploaded",
        "url": file_url
    })


# -------------------------------
# 5) SERVE UPLOADED IMAGES
# -------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# -------------------------------
# RUN (only used locally)
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
