from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Cartella in cui salvare i disegni
DRAW_DIR = "static/drawings"
os.makedirs(DRAW_DIR, exist_ok=True)

# Memorizziamo le valutazioni in memoria (basta per MVP)
evaluations = {}

# -----------------------------
# ENDPOINT PER UPLOAD DEL DISEGNO
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_image():
    match_id = request.form.get("matchID")
    word = request.form.get("word")
    image_file = request.files.get("image")

    if not match_id or not word or not image_file:
        return jsonify({"error": "missing data"}), 400

    filename = f"{match_id}.png"
    path = os.path.join(DRAW_DIR, filename)
    image_file.save(path)

    return jsonify({
        "status": "success",
        "url": f"/drawing/{filename}"
    })

# -----------------------------
# ENDPOINT PER OTTENERE IL DISEGNO
# -----------------------------
@app.route("/drawing/<filename>")
def get_drawing(filename):
    return send_from_directory(DRAW_DIR, filename)

# -----------------------------
# PAGINA WEB PER VALUTARE IL DISEGNO
# -----------------------------
@app.route("/judge/<match_id>", methods=["GET"])
def judge(match_id):
    file_path = f"/drawing/{match_id}.png"

    if not os.path.exists(os.path.join(DRAW_DIR, f"{match_id}.png")):
        return "Drawing not found", 404

    html = f"""
    <html>
    <body style='font-family: sans-serif'>
        <h2>Valutazione match: {match_id}</h2>
        <img src='{file_path}' style='width: 300px; border: 2px solid black'/><br><br>

        <form action="/submit" method="post">
            <input type="hidden" name="matchID" value="{match_id}">
            Oggetto indovinato: <input name="guess"><br><br>
            Voto (0-100): <input type="number" name="score"><br><br>
            <button type="submit">Invia Valutazione</button>
        </form>
    </body>
    </html>
    """
    return html

# -----------------------------
# ENDPOINT PER INVIARE LA VALUTAZIONE
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit_score():
    match_id = request.form.get("matchID")
    guess = request.form.get("guess")
    score = request.form.get("score")

    evaluations[match_id] = {
        "guess": guess,
        "score": int(score)
    }

    return f"Valutazione salvata! Puoi chiudere la pagina."

# -----------------------------
# ENDPOINT PER UNITY PER OTTENERE IL RISULTATO
# -----------------------------
@app.route("/result/<match_id>")
def get_result(match_id):
    if match_id not in evaluations:
        return jsonify({"ready": False})

    return jsonify({
        "ready": True,
        "score": evaluations[match_id]["score"],
        "guess": evaluations[match_id]["guess"]
    })

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)