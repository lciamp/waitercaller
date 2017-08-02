import base64, hashlib, os

x = '123456'
y = 'NRFU073fimsRVP72mmks'

def get_hash(plain):
    return hashlib.sha512(plain).hexdigest()

def validate_password(plain, salt):
    return get_hash(plain + salt)

print validate_password(x, y)