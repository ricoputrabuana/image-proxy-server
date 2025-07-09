from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Agar bisa diakses dari frontend React

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