import hashlib


def generate_hash_sha1(text):
    hash_object = hashlib.sha1(text.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


def base64_encode(text):
    header, base_64 = text.split(",")
    return base_64
