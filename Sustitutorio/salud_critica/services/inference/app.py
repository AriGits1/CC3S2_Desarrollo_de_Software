from flask import Flask, request, jsonify
import hashlib
from datetime import datetime

app = Flask(__name__)

MODEL_VERSION = "v2.3.1"
MODEL_HASH = hashlib.sha256(MODEL_VERSION.encode()).hexdigest()[:16]

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'inference',
        'model_version': MODEL_VERSION,
        'model_hash': MODEL_HASH
    })

@app.route('/infer', methods=['POST'])
def infer():
    data = request.json
    
    # Simulacion de inferencia ML
    diagnosis = "normal" if sum(data.get('signal', [0])) < 50 else "arritmia"
    
    result = {
        'patient_id': data.get('patient_id'),
        'diagnosis': diagnosis,
        'confidence': 0.89,
        'model_version': MODEL_VERSION,
        'model_hash': MODEL_HASH,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    print(f"Diagnosis: {diagnosis} for patient {data.get('patient_id')}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
