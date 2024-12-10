
def secret_key_generate():
    from os import urandom
    out = urandom(24)
    from binascii import hexlify
    secret_key = hexlify(out).decode('utf-8')
    return secret_key

if __name__ == '__main__':
    secret = secret_key_generate()
    print(secret)