from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://image-enhancer-frontend-green.vercel.app"])

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        data = request.get_json()
        image_data = data.get("data")
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Kirim ke Hugging Face
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

# ✅ Tambahkan ini agar Railway tahu port-nya
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Gunakan env PORT jika ada, default 5000
    app.run(host="0.0.0.0", port=port)
