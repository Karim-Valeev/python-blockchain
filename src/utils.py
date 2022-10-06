# from hashlib import sha256
from Crypto.Hash import SHA256


def get_bytes_hash(data: bytes) -> bytes:
    return SHA256.new(data).digest()


def get_str_hash(data: str) -> str:
    return SHA256.new(data.encode('utf-8')).hexdigest()
