import os
import psutil
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
KILL_PASSWORD = os.getenv('KILL_PASSWORD')

STARTS_WITH = ["yagna", "ya-provider"]

app = Flask(__name__)

def kill_matching(prefixes):
    killed = []
    for proc in psutil.process_iter(['name']):
        name = proc.info.get('name') or ''
        for prefix in prefixes:
            if name.startswith(prefix):
                try:
                    proc.kill()
                    print("Killed process:", name)
                    killed.append(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    print("Failed to kill process:", name)
                    pass
                break
    return killed

@app.route('/kill', methods=['GET'])
def kill_default():
    password = request.args.get('password', '')
    if not KILL_PASSWORD:
        return jsonify({'error': 'Server misconfiguration: KILL_PASSWORD not set'}), 500
    if password != KILL_PASSWORD:
        return jsonify({'error': 'Unauthorized'}), 401
    killed = kill_matching(STARTS_WITH)
    return jsonify({'killed': killed, 'prefixes': STARTS_WITH})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)