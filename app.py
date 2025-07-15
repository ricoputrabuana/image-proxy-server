from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# CORS FIX
@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

# ROUTE FIX: support /proxy dan /proxy/
@app.route("/proxy", methods=["POST", "OPTIONS"])
@app.route("/proxy/", methods=["POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return '', 204

    try:
        data = request.get_json()
        image_data = data.get("data")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Call to Hugging Face backend
        hf_response = requests.post(
            "https://ricoputra1708-image-enhancer.hf.space/predict/",
            json={"data": image_data},
            headers={"Content-Type": "application/json"}
        )

        return jsonify(hf_response.json()), hf_response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Proxy is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
