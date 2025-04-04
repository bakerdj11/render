from flask import Flask, request, jsonify

app = Flask(__name__)
colab_url = None

@app.route('/register_colab_url', methods=['POST'])
def register_colab_url():
    global colab_url
    data = request.get_json()
    url = data.get("url")
    if url:
        colab_url = url
        print(f"✅ Registered Colab URL: {url}")
        return jsonify({"status": "ok", "received": url}), 200
    return jsonify({"error": "No URL provided"}), 400

@app.route('/get_colab_url', methods=['GET'])
def get_colab_url():
    if colab_url:
        return jsonify({"url": colab_url}), 200
    return jsonify({"error": "No URL registered yet"}), 404

if __name__ == '__main__':
    app.run(debug=True)
