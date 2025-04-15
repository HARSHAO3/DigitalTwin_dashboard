from flask import Flask, request, jsonify
import pandas as pd
import datetime

app = Flask(__name__)
live_data = []

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    data['timestamp'] = datetime.datetime.now().isoformat()
    live_data.append(data)
    return jsonify({'status': 'success'}), 200

@app.route('/latest', methods=['GET'])
def get_latest():
    return jsonify(live_data[-50:])

if __name__ == '__main__':
    app.run(port=5001)
