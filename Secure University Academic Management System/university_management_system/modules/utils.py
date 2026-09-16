import os
import json
import hashlib
import bcrypt
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def _path(filename):
    return os.path.join(DATA_DIR, filename)

def load_json(filename):
    path = _path(filename)
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filename, data):
    path = _path(filename)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def compute_hash(obj):
    # Exclude any existing hash fields when computing
    if isinstance(obj, dict) and 'record_hash' in obj:
        obj = {k: v for k, v in obj.items() if k != 'record_hash'}
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def append_audit(user_id, role, action, target=None):
    logs = load_json('audit_logs.json') or []
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'user': user_id,
        'role': role,
        'action': action,
        'target': target
    }
    logs.append(entry)
    write_json('audit_logs.json', logs)

def verify_record(filename, record_key):
    data = load_json(filename)
    rec = data.get(record_key)
    if not rec:
        return True
    expected = rec.get('record_hash')
    calc = compute_hash(rec)
    return expected == calc
