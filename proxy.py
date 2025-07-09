from flask import Flask, request, jsonify
from PIL import Image
import base64
import io
from gradio_client import Client

app = Flask(__name__)

# Ganti sesuai nama Hugging Face kamu
client = Client("ricoputra1708/image-enhancer")

@app.route("/enhance", methods=["POST"])
def enhance():
    try:
        data = request.json
        base64_image = data.get("data")[0]

        # Decode base64 ke image
        image_data = base64.b64decode(base64_image.split(",")[1])
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Kirim ke Hugging Face
        result = client.predict(image, api_name="/predict")

        # Encode hasil ke base64
        buffered = io.BytesIO()
        result.save(buffered, format="PNG")
        result_base64 = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({"data": [result_base64]})
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"error": str(e)}), 500
