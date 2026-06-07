from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import time
import uuid

app = Flask(__name__)
CORS(app)

WISHES_FILE = "wishes.json"

def load_wishes():
    if not os.path.exists(WISHES_FILE):
        return []
    with open(WISHES_FILE, "r") as f:
        return json.load(f)

def save_wishes(wishes):
    with open(WISHES_FILE, "w") as f:
        json.dump(wishes, f, indent=2)

@app.route("/wishes", methods=["GET"])
def get_wishes():
    wishes = load_wishes()
    return jsonify(sorted(wishes, key=lambda w: w["ts"], reverse=True)[:50])

@app.route("/wishes", methods=["POST"])
def post_wish():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not message:
        return jsonify({"error": "Name and message are required."}), 400
    if len(name) > 40:
        return jsonify({"error": "Name too long."}), 400
    if len(message) > 280:
        return jsonify({"error": "Message too long."}), 400

    wish = {
        "id": str(uuid.uuid4()),
        "name": name,
        "message": message,
        "ts": int(time.time() * 1000)
    }
    wishes = load_wishes()
    wishes.append(wish)
    save_wishes(wishes)
    return jsonify(wish), 201

if __name__ == "__main__":
    app.run(debug=False)
