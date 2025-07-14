from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Basic CORS, tapi tetap handle OPTIONS secara eksplisit

@app.route("/proxy", methods=["POST", "OPTIONS"])
def proxy():
    # Tangani preflight CORS (OPTIONS)
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

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

        proxy_response = make_response(jsonify(response.json()), response.status_code)
        proxy_response.headers.add("Access-Control-Allow-Origin", "*")
        return proxy_response
    except Exception as e:
        err_response = make_response(jsonify({"error": str(e)}), 500)
        err_response.headers.add("Access-Control-Allow-Origin", "*")
        return err_response

@app.route("/", methods=["GET"])
def index():
    return "Proxy server is running", 200
