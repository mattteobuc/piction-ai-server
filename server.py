from flask import Flask, request, jsonify, render_template_string
import base64
import uuid

app = Flask(__name__)

# Storage in memoria dei disegni
drawings_db = {}

# ----------------------------
# ROUTE PER UPLOAD
# ----------------------------
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not data:
        return jsonify({"error": "missing JSON"}), 400

    match_id = data.get('matchID')
    word = data.get('word')
    drawing = data.get('drawing')

    if not match_id or not word or not drawing:
        return jsonify({"error": "missing data"}), 400

    # Salva nel DB in memoria
    drawings_db[match_id] = {
        "word": word,
        "drawing": drawing
    }

    return jsonify({"status": "ok"}), 200

# ----------------------------
# ROUTE PER PRENDERE IL PUNTEGGIO
# ----------------------------
@app.route('/get_score/<match_id>/<word>', methods=['GET'])
def get_score(match_id, word):
    entry = drawings_db.get(match_id)
    if not entry or entry['word'] != word:
        return jsonify({"score": 0})
    
    # Per demo: punteggio casuale
    import random
    score = random.randint(0, 100)
    return jsonify({"score": score})

# ----------------------------
# ROUTE PER REVIEW
# ----------------------------
@app.route('/review', methods=['GET'])
def review():
    # Template HTML direttamente in render_template_string
    template = """
    <!doctype html>
    <html>
    <head>
        <title>Review Drawings</title>
    </head>
    <body>
        <h1>Review Drawings</h1>
        {% for match_id, entry in drawings.items() %}
            <div style="margin-bottom:20px; border:1px solid #ccc; padding:10px;">
                <strong>Match ID:</strong> {{ match_id }}<br>
                <strong>Word:</strong> {{ entry['word'] }}<br>
                <img src="{{ entry['drawing'] | safe }}" style="max-width:300px; image-rendering:pixelated;"><br>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(template, drawings=drawings_db)

# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
