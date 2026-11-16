from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random

app = Flask(__name__, static_folder='.', static_url_path='')

# حماية من DDoS: كل IP مسموح له بـ 60 طلب في الدقيقة
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri="memory://",
)

# ... (قاعدة بيانات TOOLS_DB زي ما هي عندك، بس ضيف اللابات اللي هترفعها) ...
# عشان الكود ميطولش، هسيبك تنسخ الـ TOOLS_DB القديم هنا، أو تبعتلي أضيفه.

@app.route('/')
def index(): 
    return send_from_directory('.', 'index.html')

@app.route('/api/tools')
@limiter.limit("30 per minute")
def get_tools(): 
    return jsonify(TOOLS_DB)

@app.route('/api/deploy', methods=['POST'])
@limiter.limit("10 per minute")
def deploy_lab():
    data = request.json
    tool = data.get('tool')
    diff = data.get('diff')
    
    if tool not in TOOLS_DB:
        return jsonify({"success": False})
        
    target_url = TOOLS_DB[tool]['links'].get(diff)
    fake_ip = f"10.10.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    return jsonify({
        "success": True, 
        "url": target_url, 
        "ip": fake_ip
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
