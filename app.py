from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Tambahkan header CORS setelah setiap request
@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

# Tangani OPTIONS untuk preflight
@app.route("/proxy/", methods=["POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        # Ini penting! Jawab preflight OPTIONS dengan 204 No Content
        response = jsonify({"message": "CORS Preflight OK"})
        response.status_code = 204
        return response

    try:
        data = request.get_json()
        image_data = data.get("data")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Kirim request ke HuggingFace
        response = requests.post(
            "https://ricoputra1708-image-enhancer.hf.space/predict/",
            json={"data": [image_data]},
            headers={"Content-Type": "application/json"}
        )

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Proxy is running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
