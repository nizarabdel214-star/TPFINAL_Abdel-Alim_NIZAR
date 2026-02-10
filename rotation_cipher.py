def rotate_char(c: str, k: int) -> str:
    k = k % 26
    if 'A' <= c <= 'Z':
        base = ord('A')
        return chr(base + (ord(c) - base + k) % 26)
    if 'a' <= c <= 'z':
        base = ord('a')
        return chr(base + (ord(c) - base + k) % 26)
    return c


def encrypt(text: str, k: int) -> str:
    return ''.join(rotate_char(c, k) for c in text)


def decrypt(text: str, k: int) -> str:
    return ''.join(rotate_char(c, -k) for c in text)


def main():
    mode = input("Mode (encrypt/decrypt): ").strip().lower()
    text = input("Message: ")
    k = int(input("Clé (entier): "))

    if mode == "encrypt":
        print("Chiffré:", encrypt(text, k))
    elif mode == "decrypt":
        print("Déchiffré:", decrypt(text, k))
    else:
        print("Mode invalide.")


if __name__ == "__main__":
    main()
