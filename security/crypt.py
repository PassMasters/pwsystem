import base64
import os
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pwmanager.models import PW, Encryption, Data_ID
def decrypt( obj, key):
        ks = Fernet(key)
        v2 = bytes(obj.Password, 'utf-8')
        v1 = str(ks.decrypt(v2), 'utf-8')
        x1 = bytes(obj.TOTP, 'utf-8')
        x2 = str(ks.decrypt(x1), 'utf-8')
        form_initial = {
            'Password': v1,
            'TOTP': x2
            }
        return form_initial

def encrypt(obj, key):
    ks = Fernet(key)
    v1 = bytes(obj, 'UTF-8')
    v2 = ks.encrypt(v1)
    return v2
