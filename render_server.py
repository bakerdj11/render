from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes and origins

colab_url = None  # Global variable to store the received URL

@app.route('/')
def index():
    return 'Colab URL Server is running!'

@app.route('/register_colab_url', methods=['POST'])
def register_colab_url():
    global colab_url
    data = request.get_json()
    colab_url = data.get('url')
    print("✅ Received Colab URL:", colab_url)
    return jsonify({"status": "ok", "url": colab_url})

@app.route('/get_colab_url', methods=['GET'])
def get_colab_url():
    if colab_url:
        return jsonify({"url": colab_url})
    return jsonify({"error": "No Colab URL registered yet"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
