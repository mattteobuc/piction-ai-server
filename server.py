from flask import Flask, request, jsonify, render_template_string
import base64

app = Flask(__name__)

# Storage semplice in memoria
drawings_db = {}   # {matchID: {'word':..., 'drawing':..., 'score':..., 'subject':...}}

# -----------------------------
# ROUTE UPLOAD
# -----------------------------
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not data or 'matchID' not in data or 'word' not in data or 'drawing' not in data:
        return jsonify({"error": "missing data"}), 400

    matchID = data['matchID']
    drawings_db[matchID] = {
        'word': data['word'],
        'drawing': data['drawing'],
        'score': None,
        'subject': None
    }

    return jsonify({"status": "ok"}), 200

# -----------------------------
# ROUTE GET SCORE
# -----------------------------
@app.route('/get_score/<matchID>/<word>', methods=['GET'])
def get_score(matchID, word):
    entry = drawings_db.get(matchID)
    if not entry or entry['word'] != word:
        return jsonify({"error": "not found"}), 404
    score = entry['score'] if entry['score'] is not None else 0
    return jsonify({"score": score})

# -----------------------------
# ROUTE REVIEW PAGE
# -----------------------------
@app.route('/review', methods=['GET'])
def review_page():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Review Drawings</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            .drawing { border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }
            img { max-width: 200px; display: block; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Review Drawings</h1>
        {% for matchID, entry in drawings.items() %}
            <div class="drawing">
                <strong>Match ID:</strong> {{ matchID }}<br>
                <strong>Word:</strong> {{ entry['word'] }}<br>
                <img src="{{ entry['drawing'] }}"><br>
                <form action="/submit_score" method="post">
                    <input type="hidden" name="matchID" value="{{ matchID }}">
                    <input type="hidden" name="word" value="{{ entry['word'] }}">
                    Subject: <input type="text" name="subject" value="{{ entry['subject'] or '' }}"><br>
                    Score: <input type="number" name="score" value="{{ entry['score'] or '' }}"><br>
                    <button type="submit">Submit</button>
                </form>
            </div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(html, drawings=drawings_db)

# -----------------------------
# ROUTE SUBMIT SCORE
# -----------------------------
@app.route('/submit_score', methods=['POST'])
def submit_score():
    matchID = request.form.get('matchID')
    score = request.form.get('score')
    subject = request.form.get('subject')

    if not matchID or score is None:
        return "Missing data", 400

    entry = drawings_db.get(matchID)
    if not entry:
        return "MatchID not found", 404

    try:
        entry['score'] = int(score)
    except ValueError:
        return "Invalid score", 400
    entry['subject'] = subject
    return "Score submitted! <a href='/review'>Back to review</a>"

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
