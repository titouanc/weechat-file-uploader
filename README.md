# weechat-file-uploader

This is a minimal application that serves as a server-side backend for the
file upload functionality of the Weechat Android application. All uploaded
files are put in the same directory on the server. The file names are determined
by a configurable hashing algorithm, based on the content of the uploaded files.

Access to the upload functionality is limited to a list of predefined users.

## Usage

#### `GET /ping`

This endpoint allows to check whether the server is up && running. It only
replies with the text `pong`.

Example:

```bash
curl https://my.upload.server/ping
```

#### `POST /`

This is the endpoint to upload new files. It requires an HTTP basic auth, and
a `file` form field:

```bash
curl -u username --form file=@/path/to/your/file.gif https://my.upload.server/
```

## Installation

```bash
git clone https://github.com/titouanc/weechat-file-uploader
cd weechat-file-uploader
python3 -m venv ve3
source ve3/bin/activate
pip install -r requirements.txt
```

## Configuration and deployment

Create your local configuration:

```bash
grep __LOCAL__ settings.py > local_settings.py
nano local_settings.py
```

### Managing users

To add new users to the authorized list, ask them to run the following command:
```bash
python -c 'import hashlib, getpass; print(hashlib.sha512(getpass.getpass("Enter your password: ").encode()).hexdigest())'
```

Then, add the pair `"username": "hash"` into `AUTHORIZED_USERS`.

### Web server

It is **highly recommended** to serve the application using a webserver, such as
nginx. This allows to use HTTPS, which is desirable because the credentials are
transmitted with HTTP basic auth. You can easily obtain an SSL certificate with
Let's Encrypt.

Here is an example configuration file to start with nginx:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name my.server.name;
    client_max_body_size 25M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Make this file available in `/etc/nginx/sites-enabled`, then reload nginx
(`systemctl reload nginx`).

Now, your server is publicly accesible in HTTP (not secure), so let's get a
certificate:

```bash
certbot --nginx
```

Finally, start the actual application:

```bash
gunicorn app:app -b 127.0.0.1:5000
```

### Supervising with systemd

Assuming that you are running the application as the user `uploader`, you can
create the following file in `/etc/systemd/system/weechat-file-uploader.service`:

```systemd
[Unit]
Description=weechat-file-uploader
After=network.target

[Service]
Type=notify
# the specific user that our service will run as
User=uploader
Group=uploader
RuntimeDirectory=gunicorn
WorkingDirectory=/home/uploader/weechat-file-uploader
ExecStart=/home/uploader/weechat-file-uploader/ve3/bin/gunicorn app:app -b 127.0.0.1:5000
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

Then run:

```bash
systemctl reload-daemon
systemctl start weechat-file-uploader
```