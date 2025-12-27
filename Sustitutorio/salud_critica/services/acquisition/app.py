from flask import Flask, request, jsonify
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)

class DataStore:
    """Almacenamiento simple de señales"""
    def __init__(self):
        self.signals = []
    
    def save(self, patient_id, data):
        signal = {
            'patient_id': patient_id,
            'data': data,
            'timestamp': datetime.utcnow().isoformat(),
            'hash': hashlib.sha256(json.dumps(data).encode()).hexdigest()
        }
        self.signals.append(signal)
        print(f"Signal stored: {patient_id}")
        return signal['hash']

store = DataStore()

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'acquisition'})

@app.route('/acquire', methods=['POST'])
def acquire():
    data = request.json
    signal_hash = store.save(data['patient_id'], data['signal'])
    return jsonify({'status': 'acquired', 'hash': signal_hash})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
