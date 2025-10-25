# render_server.py

import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COLAB_COMFYUI_URL_PATH = "colab_comfyui_url.txt"
COLAB_FLASK_API_URL_PATH = "colab_flask_api_url.txt"
LOCAL_FLASK_API_URL_PATH = "local_flask_api_url.txt"

def write_url_atomic(filepath, url):
    """Write URL atomically with timestamp for freshness checking"""
    timestamp = time.time()
    content = f"{url}\n{timestamp}"
    
    # Write to temp file first, then rename (atomic on Unix)
    temp_path = f"{filepath}.tmp"
    with open(temp_path, "w") as f:
        f.write(content)
        f.flush()  # Force write to disk
        os.fsync(f.fileno())  # Force OS to write to disk
    
    # Atomic rename
    os.replace(temp_path, filepath)
    print(f"✅ Wrote {filepath}: {url} at {timestamp}")

def read_url_with_check(filepath, max_age_seconds=300):
    """Read URL and check if it's fresh (backward compatible with old format)"""
    if not os.path.exists(filepath):
        return None, "File not found"
    
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            lines = content.split('\n')
            
            if len(lines) == 1:
                # Old format (just URL, no timestamp) - accept it but warn
                url = lines[0]
                print(f"⚠️ {filepath} using old format (no timestamp), accepting it")
                return url, None
            elif len(lines) >= 2:
                # New format (URL + timestamp)
                url = lines[0]
                try:
                    timestamp = float(lines[1])
                    age = time.time() - timestamp
                    
                    if age > max_age_seconds:
                        print(f"⚠️ URL in {filepath} is {age:.1f}s old (stale)")
                        return None, f"URL too old ({age:.1f}s)"
                    
                    return url, None
                except ValueError:
                    # Couldn't parse timestamp, treat as old format
                    print(f"⚠️ {filepath} has invalid timestamp, using URL anyway")
                    return lines[0], None
            else:
                return None, "Empty file"
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None, str(e)

@app.route('/')
def index():
    return 'Colab URL Server is running!'

@app.route('/register_colab_comfyui_url', methods=['POST'])
def register_colab_comfyui_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        write_url_atomic(COLAB_COMFYUI_URL_PATH, url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_colab_comfyui_url', methods=['GET'])
def get_colab_comfyui_url():
    url, error = read_url_with_check(COLAB_COMFYUI_URL_PATH)
    if url:
        return jsonify({"url": url})
    return jsonify({"error": error or "No URL registered"}), 404

@app.route('/register_colab_flask_api_url', methods=['POST'])
def register_colab_flask_api_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        write_url_atomic(COLAB_FLASK_API_URL_PATH, url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_colab_flask_api_url', methods=['GET'])
def get_colab_flask_api_url():
    url, error = read_url_with_check(COLAB_FLASK_API_URL_PATH)
    if url:
        return jsonify({"url": url})
    return jsonify({"error": error or "No URL registered"}), 404

@app.route('/register_local_flask_api_url', methods=['POST'])
def register_local_flask_api_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        write_url_atomic(LOCAL_FLASK_API_URL_PATH, url)
        return jsonify({"status": "ok", "url": url})
    return jsonify({"error": "Missing URL"}), 400

@app.route('/get_local_flask_api_url', methods=['GET'])
def get_local_flask_api_url():
    url, error = read_url_with_check(LOCAL_FLASK_API_URL_PATH)
    if url:
        return jsonify({"url": url})
    return jsonify({"error": error or "No URL registered"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
