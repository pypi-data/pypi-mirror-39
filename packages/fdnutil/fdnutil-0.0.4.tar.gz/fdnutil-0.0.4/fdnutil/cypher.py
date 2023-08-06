from cryptography.fernet import Fernet

import logging
from fdnutil.whoami import iam
logger = logging.getLogger(name=iam())

def encrypt(text, key):
    f = Fernet(key)
    return f.encrypt(text)

def decrypt(encrypted_text, key):
    f = Fernet(key)
    return f.decrypt(encrypted_text)