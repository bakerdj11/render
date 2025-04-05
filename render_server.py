from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🧠 Store both URLs
comfy_url = None
flask_api_url = None

@app.route('/')
def index():
    return "Render callback server is running!"

# ✅ Register both ComfyUI and Flask API URLs
@app.route('/register_colab_url', methods=['POST'])
def register_colab_url():
    global comfy_url, flask_api_url
    data = request.get_json()

    if "comfy" in data:
        comfy_url = data["comfy"]
        print("✅ Registered ComfyUI URL:", comfy_url)

    if "api" in data:
        flask_api_url = data["api"]
        print("✅ Registered Mini Flask API URL:", flask_api_url)

    return jsonify({"status": "ok"})

# 📤 Endpoint for local Flask to fetch both
@app.route('/get_colab_url', methods=['GET'])
def get_colab_url():
    if not comfy_url and not flask_api_url:
        return jsonify({"error": "No URLs registered yet"}), 404

    return jsonify({
        "comfy": comfy_url,
        "api": flask_api_url
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
