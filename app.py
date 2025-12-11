from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

# Folder to store uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store status in memory (simple solution)
status_data = {
    "status": "Waiting for Pi...",
    "timestamp": "",
    "last_image": ""
}

# -----------------------------
# API ROUTES
# -----------------------------

@app.route("/")
def home():
    return "Breathalyzer API Running"

@app.route("/status", methods=["GET"])
def get_status():
    """Dashboard fetches this"""
    return jsonify(status_data)

@app.route("/update_status", methods=["POST"])
def update_status():
    """Pi sends status updates"""
    global status_data
    data = request.json
    status_data.update(data)
    return jsonify({"message": "Status updated"}), 200

@app.route("/upload_image", methods=["POST"])
def upload_image():
    """Pi uploads image here"""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filename = f"img_{int(time.time())}.jpg"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(save_path)

    # Public URL for the dashboard
    file_url = f"https://breathalyzer-api.onrender.com/uploads/{filename}"

    # update last_image
    status_data["last_image"] = file_url

    return jsonify({"url": file_url})
    
# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return app.send_static_file(f"../uploads/{filename}")


# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
