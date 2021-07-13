from os import path
import hashlib

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

from settings import FILE_UPLOAD_DIR, FILE_PUBLIC_URL, FILE_HASH_ALGO, AUTHORIZED_USERS


file_hash_algo = getattr(hashlib, FILE_HASH_ALGO)
auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.verify_password
def auth_user(username, password):
    if username in AUTHORIZED_USERS:
        hashed = hashlib.sha512(password.encode()).hexdigest()
        return AUTHORIZED_USERS[username] == hashed
    return False


@app.route('/', methods=['POST'])
@auth.login_required
def upload():
    assert request.method == 'POST'

    f = request.files['file']
    name = file_hash_algo(f.stream.read()).hexdigest()
    ext = f.filename.split('.', 1)[-1]
    save_name = f"{name}.{ext}"

    f.stream.seek(0)
    f.save(path.join(FILE_UPLOAD_DIR, save_name))
    return path.join(FILE_PUBLIC_URL, save_name)


@app.route('/ping')
def ping():
    return "pong"
