from flask import Flask, request, jsonify, make_response
import requests
import os  # ← tambahkan ini

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

@app.route("/proxy", methods=["POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return '', 204

    try:
        data = request.get_json()
        image_data = data.get("data")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        response = requests.post(
            "https://ricoputra1708-image-enhancer.hf.space/predict/",
            json={"data": [image_data]},
            headers={"Content-Type": "application/json"}
        )

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Proxy server is running", 200

# ⬇️ INI BAGIAN PENTING UNTUK RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
