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

@app.route('/register_colab_url', methods=['POST'])
def register_colab_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(COLAB_URL_PATH, "w") as f:
            f.write(url)
        print("✅ Saved Colab URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "No URL provided"}), 400

@app.route('/get_colab_url', methods=['GET'])
def get_colab_url():
    if os.path.exists(COLAB_URL_PATH):
        with open(COLAB_URL_PATH, "r") as f:
            url = f.read().strip()
        return jsonify({"url": url})
    return jsonify({"error": "No Colab URL registered yet"}), 404

@app.route('/register_flask_api_url', methods=['POST'])
def register_flask_api_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(FLASK_API_URL_PATH, "w") as f:
            f.write(url)
        print("✅ Saved Flask API URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "No URL provided"}), 400

@app.route('/get_flask_api_url', methods=['GET'])
def get_flask_api_url():
    if os.path.exists(FLASK_API_URL_PATH):
        with open(FLASK_API_URL_PATH, "r") as f:
            url = f.read().strip()
        return jsonify({"url": url})
    return jsonify({"error": "No Flask API URL registered yet"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
