from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Mengizinkan semua origin (terbuka untuk testing)

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        data = request.get_json()
        image_data = data.get("data")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Kirim request ke backend Hugging Face
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

# Bagian penting agar Railway bisa menjalankan app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Gunakan port dari Railway
    app.run(host="0.0.0.0", port=port)
