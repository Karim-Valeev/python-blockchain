# from hashlib import sha256
import requests
from typing import Tuple, Optional

from Crypto.Hash import SHA256

from config.settings import settings


def get_bytes_hash(data: bytes) -> bytes:
    return SHA256.new(data).digest()


def get_str_hash(data: bytes) -> str:
    # return SHA256.new(data.encode('utf-8')).hexdigest()
    return SHA256.new(data).hexdigest()


def get_arbiter_public_key() -> Optional[bytes]:
    response = requests.get(settings.ARBITER_URL + "/ts/public")
    if response.status_code == 200:
        return response.content
    else:
        return None


def get_ts_and_signature_from_arbiter(hash_hexdigest: str) -> Tuple[str, bytes]:
    response = requests.get(
        settings.ARBITER_URL + "/ts",
        {"digest": hash_hexdigest}
    )
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 0:
            return data["timeStampToken"]['ts'], data["timeStampToken"]['signature']


