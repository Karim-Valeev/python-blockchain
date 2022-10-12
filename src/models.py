from typing import List

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import PKCS1_PSS

from utils import get_bytes_hash, get_str_hash, get_ts_and_signature_from_arbiter


class Block:
    number: int
    previous_block_hash: bytes
    data: List[str]  # aka transactions
    block_signature: bytes  # from previous_block_hash and data
    arbiter_signature: bytes  # from previous_block_hash, data and block_signature
    arbiter_signature_timestamp: str

    def __init__(self, number, previous_block_hash, data, block_signature) -> None:
        self.number = number
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.block_signature = block_signature
        self.arbiter_signature_timestamp = ''
        self.arbiter_signature = b''

    def __str__(self):
        return '<Block: number = %s, previous_block_hash = %s, data = %s, signature = %s>, arbiter_signature_timestamp = %s, arbiter_signature=%s' % (
            self.number, self.previous_block_hash, self.data, self.block_signature,
            self.arbiter_signature_timestamp, self.arbiter_signature
        )

    def get_block_info_hash_digest(self) -> bytes:
        pass

    def get_block_info_hash_hexdigest(self) -> str:
        payload = self.previous_block_hash + ''.join(self.data).encode("utf-8") + self.block_signature
        return get_str_hash(payload)


class KeyPair:
    private_key: RsaKey
    public_key: RsaKey

    def __init__(self) -> None:
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

    def __str__(self):
        return '<KeyPait: Private key: %s \nPublic key %s>' % (
            self.private_key.exportKey().decode("utf-8"),
            self.public_key.exportKey().decode("utf-8")
        )


class BlockChain:
    name: str
    blockchain_initial_length: int
    blockchain: List[Block]
    key_pair: KeyPair
    transaction_cache: List[str]

    def __init__(self, name, blockchain_initial_length, key_pair, transaction_cache) -> None:
        self.name = name
        self.blockchain_initial_length = blockchain_initial_length
        self.key_pair = key_pair
        self.transaction_cache = transaction_cache
        self.blockchain = []

    def _generate_rsa_pss_signature(self, data: bytes) -> bytes:
        hasher = SHA256.new(data)
        signer = PKCS1_PSS.new(self.key_pair.private_key)
        return signer.sign(hasher)

    def _verify_rsa_pss_signature(self, data: bytes, signature: bytes) -> bool:
        hasher = SHA256.new(data)
        verifier = PKCS1_PSS.new(self.key_pair.public_key)
        return verifier.verify(hasher, signature)

    def initiate_block_chain(self):
        previous_block_hash = b''
        for i in range(self.blockchain_initial_length):
            block = Block(
                i,
                previous_block_hash,
                [self.transaction_cache[i]],
                self._generate_rsa_pss_signature(previous_block_hash),
            )
            block.arbiter_signature_timestamp, block.arbiter_signature = get_ts_and_signature_from_arbiter(
                block.get_block_info_hash_hexdigest()
            )
            # Find hash from previous block hash and data
            previous_block_hash = get_bytes_hash(
                block.previous_block_hash + ''.join(block.data).encode("utf-8")
            )
            self.blockchain.append(block)

    def is_verified(self) -> bool:
        previous_block_hash = get_bytes_hash(
                self.blockchain[0].previous_block_hash + ''.join(self.blockchain[0].data).encode("utf-8")
            )
        for i in range(1, len(self.blockchain)):
            block = self.blockchain[i]
            if not previous_block_hash == block.previous_block_hash:
                return False

            previous_block_hash = get_bytes_hash(
                block.previous_block_hash + ''.join(block.data).encode("utf-8")
            )

            if not self._verify_rsa_pss_signature(block.previous_block_hash, block.block_signature):
                return False
        return True

    def damage_block(self, number):
        self.blockchain[number].data = ["...damaged data..."]

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def __str__(self):
        result = f'{self.name}\n'
        for block in self.blockchain:
            result += str(block) + '\n'
        return result



