from sha3 import keccak_256


def sha3(seed):
    #hash = keccak_256(seed).digest()
    return keccak_256(seed).digest()


def keccak_hash(seed):
    return keccak_256(seed).digest()