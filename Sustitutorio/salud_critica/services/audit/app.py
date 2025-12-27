from flask import Flask, request, jsonify
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)

class AuditLog:
    """Registro de auditoria con firma simple"""
    def __init__(self):
        self.events = []
    
    def record(self, event_type, details):
        event = {
            'event_id': hashlib.sha256(str(datetime.utcnow()).encode()).hexdigest()[:16],
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details
        }
        # Firma simple con hash
        event['signature'] = hashlib.sha256(
            json.dumps(event, sort_keys=True).encode()
        ).hexdigest()
        
        self.events.append(event)
        print(f"Event recorded: {event_type} - {event['event_id']}")
        return event['event_id']

audit = AuditLog()

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'audit'})

@app.route('/audit', methods=['POST'])
def record_audit():
    data = request.json
    event_id = audit.record(data['event_type'], data['details'])
    return jsonify({'event_id': event_id, 'status': 'recorded'})

@app.route('/query')
def query_audit():
    return jsonify({'total': len(audit.events), 'events': audit.events[-10:]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
