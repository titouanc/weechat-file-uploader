FILE_UPLOAD_DIR = '/some/directory'
FILE_PUBLIC_URL = 'https://localhost'
AUTHORIZED_USERS = {
    # username: sha512(password).hexdigest()
}

try:
    from local_settings import *
except ImportError:
    print("No local settings !")
