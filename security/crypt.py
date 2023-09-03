import base64
import os
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pwmanager.models import PW, Encryption, Data_ID, PWcheck
from Crypto.Cipher import AES
def check(user, key):
    dID = Data_ID.objects.get(User=user)
    ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
    PWcheck2 = PWcheck.objects.get(Owner_ID=dID.Key_lookup) 
    EPW = bytes(PWcheck2.Test_PW,'UTF-8')
    EPW2 = eval(EPW)
    EPW = EPW2
    Ans = PWcheck2.Answer
    iv = bytes(ekey.IV,'UTF-8')
    print(iv)
    print(len(iv))
    iv2 = eval(iv)
    print(iv2)
    iv = iv2
    keys = AES.new(key, AES.MODE_CBC, iv)
    test = EPW
    decrypted = keys.decrypt(test)
    padding_length = decrypted[-1]
    integer_bytes = decrypted[:-padding_length]
    decrypted_integer = int.from_bytes(integer_bytes, byteorder='big')
    if decrypted_integer == Ans:
        return True
    else:
        return False 
def decrypt( obj, key, user):
        dID = Data_ID.objects.get(User=user)
        ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
        PWcheck2 = PWcheck.objects.get(Owner_ID=dID.Key_lookup) 
        v7 = eval(bytes(obj.Password, 'UTF-8'))
        iv = eval(bytes(ekey.IV, 'UTF-8'))
        keys = AES.new(key, AES.MODE_CBC, iv)
        x0 = keys.decrypt(v7)
        padding_length = x0[-1]
        plaintext_bytes = x0[:-padding_length]
        v2 = str(plaintext_bytes,'UTF-8')
        try:
              
            x1 = eval(bytes(obj.TOTP, 'utf-8'))
            x2 = keys.decrypt(x1)
            padding_length = x2[-1]
            plaintext_bytes = x2[:-padding_length]
            x3 = str(plaintext_bytes,'UTF-8')
        except Exception as e:
             from_initial = {
                  'Password': v2,
                  'TOTP': "N/A"
             }
             return from_initial
        form_initial = {
            'Password': v2,
            'TOTP': x3
            }
        return form_initial

def encrypt(obj, key, user):
    dID = Data_ID.objects.get(User=user)
    ekey = Encryption.objects.get(Owner_ID=dID.Key_lookup)
    iv = bytes(ekey.IV, 'UTF-8')
    keys = AES.new(key, AES.MODE_CBC, iv)
    PWcheck2 = PWcheck.objects.get(Owner_ID=dID.Key_lookup) 
    check2 = check(user, key)
    if check2 != True:
        raise Exception("key check failure")
    
    v1 = bytes(obj, 'UTF-8')
    padding_length = 16 - (len(v1) % 16)
    plaintext_bytes += bytes([padding_length]) * padding_length
    v2 = keys.encrypt(plaintext_bytes)
    return v2
