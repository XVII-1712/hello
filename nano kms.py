from flask import Flask, request, jsonify

app = Flask(__name__)
keys = {}

@app.route('/keys', methods=['POST'])
def store_key():
    data = request.get_json()
    keys[data['id']] = data['key']
    return jsonify({"message": "Key stored successfully"})

@app.route('/keys/<id>', methods=['GET'])
def get_key(id):
    key = keys.get(id)
    if key is None:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
