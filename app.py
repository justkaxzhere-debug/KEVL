from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import uuid
import requests

app = Flask(__name__)
CORS(app)

SUPABASE_URL = "https://ekumdprtrzvhirhbvjtv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrdW1kcHJ0cnp2aGlyaGJ2anR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA4MjgwMTMsImV4cCI6MjA5NjQwNDAxM30.fsRaMesUaD1OoDgd7tvU8R6yAklhKDxsRcyOpXiJz4s"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route("/wishes", methods=["GET"])
def get_wishes():
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/wishes?order=ts.desc&limit=50",
        headers=HEADERS
    )
    return jsonify(res.json()), res.status_code

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
    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/wishes",
        headers={**HEADERS, "Prefer": "return=representation"},
        json=wish
    )
    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    app.run(debug=False)
    
