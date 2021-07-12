from os import path
from hashlib import sha256, sha512

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

from settings import FILE_UPLOAD_DIR, FILE_PUBLIC_URL, AUTHORIZED_USERS


auth = HTTPBasicAuth()


@auth.verify_password
def auth_user(username, password):
    if username in AUTHORIZED_USERS:
        hashed = sha512(password.encode()).hexdigest()
        return AUTHORIZED_USERS[username] == hashed
    return False


app = Flask(__name__)


@app.route('/', methods=['POST'])
@auth.login_required
def upload():
    assert request.method == 'POST'

    f = request.files['file']
    name = sha256(f.stream.read()).hexdigest()
    ext = f.filename.split('.', 1)[-1]
    save_name = f"{name}.{ext}"

    f.stream.seek(0)
    f.save(path.join(FILE_UPLOAD_DIR, save_name))
    return path.join(FILE_PUBLIC_URL, save_name)


@app.route('/ping')
def ping():
    return "pong"
