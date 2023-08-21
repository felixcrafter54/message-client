import os
import sys
import hashlib

# Get the path of the script and construct the absolute path to the image
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def hash_password(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()