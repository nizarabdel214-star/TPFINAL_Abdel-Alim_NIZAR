# block_cipher.py
import os

BLOCK_SIZE = 16

def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Données vides")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Padding invalide")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Padding invalide")
    return data[:-pad_len]

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def normalize_key(key_str: str, size: int = BLOCK_SIZE) -> bytes:
    key = key_str.encode("utf-8")
    if len(key) >= size:
        return key[:size]
    return key + bytes(size - len(key))

def encrypt_block(block: bytes, key: bytes) -> bytes:
    return xor_bytes(block, key)

def decrypt_block(block: bytes, key: bytes) -> bytes:
    return xor_bytes(block, key)

def encrypt_ecb(plaintext: bytes, key: bytes) -> bytes:
    plaintext = pkcs7_pad(plaintext)
    out = bytearray()
    for i in range(0, len(plaintext), BLOCK_SIZE):
        out += encrypt_block(plaintext[i:i+BLOCK_SIZE], key)
    return bytes(out)

def decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes:
    out = bytearray()
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        out += decrypt_block(ciphertext[i:i+BLOCK_SIZE], key)
    return pkcs7_unpad(bytes(out))

def encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    plaintext = pkcs7_pad(plaintext)
    out = bytearray()
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        x = xor_bytes(block, prev)
        c = encrypt_block(x, key)
        out += c
        prev = c
    return bytes(out)

def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    out = bytearray()
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        p = xor_bytes(decrypt_block(block, key), prev)
        out += p
        prev = block
    return pkcs7_unpad(bytes(out))

def main():
    message = "Bonjour tout le monde, ceci est un test."
    key_str = "secret"
    key = normalize_key(key_str)

    plaintext = message.encode("utf-8")

    print("=== ECB ===")
    c_ecb = encrypt_ecb(plaintext, key)
    print("Cipher (hex):", c_ecb.hex())
    print("Déchiffré:", decrypt_ecb(c_ecb, key).decode())

    print("\n=== CBC ===")
    iv = os.urandom(BLOCK_SIZE)
    c_cbc = encrypt_cbc(plaintext, key, iv)
    print("IV (hex):", iv.hex())
    print("Cipher (hex):", c_cbc.hex())
    print("Déchiffré:", decrypt_cbc(c_cbc, key, iv).decode())

if __name__ == "__main__":
    main()
