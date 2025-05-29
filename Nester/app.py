from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Data received: {data}")
    return jsonify({"status": "success", "received_data": data}), 200

@app.route('/', methods=['GET'])
def home():
    return "API Flask en marche ! Utilisez POST /api/data pour envoyer des données."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
