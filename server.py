from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Legge il body della richiesta
    data = request.get_json(force=True, silent=True)
    
    # Log completo del body ricevuto
    print("BODY RICEVUTO:", request.data)
    print("JSON PARSATO:", data)

    # Controlli
    if not data:
        return jsonify({"error": "missing data"}), 400

    required_fields = ["matchID", "word", "drawing"]
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"Manca il campo: {field}")
            return jsonify({"error": f"missing {field}"}), 400

    # Se tutto ok
    print("Ricevuto disegno per matchID:", data["matchID"])
    return jsonify({"message": "Disegno ricevuto correttamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
