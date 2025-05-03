# render_server.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COLAB_URL_PATH = "colab_url.txt"
FLASK_API_URL_PATH = "flask_api_url.txt"

@app.route('/')
def index():
    return 'Colab URL Server is running!'
COLAB_COMFYUI_URL_PATH = "colab_comfyui_url.txt"
COLAB_FLASK_API_URL_PATH = "colab_flask_api_url.txt"
LOCAL_FLASK_API_URL_PATH = "local_flask_api_url.txt"

@app.route('/register_colab_comfyui_url', methods=['POST'])
def register_colab_comfyui_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(COLAB_COMFYUI_URL_PATH, "w") as f:
            f.write(url)
        print("✅ Registered COLAB_COMFYUI_URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_colab_comfyui_url', methods=['GET'])
def get_colab_comfyui_url():
    if os.path.exists(COLAB_COMFYUI_URL_PATH):
        with open(COLAB_COMFYUI_URL_PATH, "r") as f:
            return jsonify({"url": f.read().strip()})
    return jsonify({"error": "No Colab ComfyUI URL registered yet"}), 404

@app.route('/register_colab_flask_api_url', methods=['POST'])
def register_colab_flask_api_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(COLAB_FLASK_API_URL_PATH, "w") as f:
            f.write(url)
        print("✅ Registered COLAB_FLASK_API_URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_colab_flask_api_url', methods=['GET'])
def get_colab_flask_api_url():
    if os.path.exists(COLAB_FLASK_API_URL_PATH):
        with open(COLAB_FLASK_API_URL_PATH, "r") as f:
            return jsonify({"url": f.read().strip()})
    return jsonify({"error": "No Colab Flask API URL registered yet"}), 404

@app.route('/register_local_flask_api_url', methods=['POST'])
def register_local_flask_api_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(LOCAL_FLASK_API_URL_PATH, "w") as f:
            f.write(url)
        print("✅ Registered LOCAL_FLASK_API_URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_local_flask_api_url', methods=['GET'])
def get_local_flask_api_url():
    if os.path.exists(LOCAL_FLASK_API_URL_PATH):
        with open(LOCAL_FLASK_API_URL_PATH, "r") as f:
            return jsonify({"url": f.read().strip()})
    return jsonify({"error": "No Local Flask API URL registered yet"}), 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
