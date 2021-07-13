# Directory on the local filesystem where the files should be uploaded
FILE_UPLOAD_DIR = '/some/directory'  # __LOCAL__

# Public URL at which the uploaded diles are served
FILE_PUBLIC_URL = 'http://localhost'  # __LOCAL__

# The hashing algorithm to determine the uploaded file name
FILE_HASH_ALGO = 'sha256'  # __LOCAL__

# List of users:password that are allowed to upload on this app
AUTHORIZED_USERS = {  # __LOCAL__
    # username: sha512(password).hexdigest()  # __LOCAL__
}  # __LOCAL__

try:
    from local_settings import *
except ImportError:
    print("No local settings !")
