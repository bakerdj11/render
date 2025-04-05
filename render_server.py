# render_server.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STORAGE_PATH = "colab_url.txt"

@app.route('/')
def index():
    return 'Colab URL Server is running!'

@app.route('/register_colab_url', methods=['POST'])
def register_colab_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        with open(STORAGE_PATH, "w") as f:
            f.write(url)
        print("✅ Saved Colab URL:", url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "No URL provided"}), 400

@app.route('/get_colab_url', methods=['GET'])
def get_colab_url():
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "r") as f:
            url = f.read().strip()
        return jsonify({"url": url})
    return jsonify({"error": "No Colab URL registered yet"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
