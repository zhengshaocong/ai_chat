from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# 获取static目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__)
# 允许跨域访问
CORS(app)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    app.run(port=9000, debug=True) 