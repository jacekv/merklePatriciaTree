from sha3 import keccak_256


def sha3(seed):
    return keccak_256(seed).digest()


def keccak_hash(seed):
    return keccak_256(seed).digest()