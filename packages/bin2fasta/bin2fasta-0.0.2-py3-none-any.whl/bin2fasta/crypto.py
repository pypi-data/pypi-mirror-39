import os
from io import IOBase

import M2Crypto


class CryptoStreamer(IOBase):
    def __init__(self, key: str, fname: str):
        self.stream = stream

        block_size = M2Crypto.m2.AES_BLOCK_SIZE
        iv = os.urandom(block_size)

        self.aes = M2Crypto.EVP.Cipher(
            alg='aes_128_cfb',
            key=key.encode(),
            iv=iv,
            op=M2Crypto.m2.encrypt
        )

    def read(self, *args, **kwargs):
        return self.aes.update(self.stream.read(*args, **kwargs))

    def write(self, data):
        self.stream.write(self.aes.update(data.encode()))

    def close(self):
        self.stream.write(self.aes.final())


if __name__ == '__main__':
    import sys
    cs = CryptoStreamer('huibuh', sys.stdout)
    cs.write('foo')
