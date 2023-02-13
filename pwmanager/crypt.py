import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import json

def encrypt (pin, input, output,salt):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(pin))
        e = Fernet(key)
        h = bytes(input, 'UTF-8')
        k = e.encrypt(h)
        s = str(k, 'UTF-8')
        return s

def decrypt (pin, input, output,salt):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),     length=32,  salt=salt,   iterations=100000, )
        key = base64.urlsafe_b64encode(kdf.derive(pin))
        e = Fernet(key)
        h = bytes(input, 'UTF-8')
        k = e.encrypt(h)
        s = str(k, 'UTF-8')
        return s

        
        
