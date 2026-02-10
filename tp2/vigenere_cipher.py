def vigenere(message, key, mode):
    result = ""
    key = key.lower()
    key_index = 0

    for char in message:
        if char.isalpha():
            # Position de la lettre de la clé (0-25)
            shift = ord(key[key_index % len(key)]) - ord('a')

            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            letter_index = ord(char) - base

            if mode == "encrypt":
                new_index = (letter_index + shift) % 26
            else:  # decrypt
                new_index = (letter_index - shift) % 26

            result += chr(base + new_index)
            key_index += 1
        else:
            result += char

    return result


# -------- PROGRAMME PRINCIPAL --------

mode = input("Mode (encrypt/decrypt) : ").lower()

if mode not in ["encrypt", "decrypt"]:
    print("❌ Mode invalide")
    exit()

message = input("Message : ")
key = input("Clé : ")

if not key.isalpha():
    print("❌ La clé doit contenir uniquement des lettres")
    exit()

output = vigenere(message, key, mode)
print("Résultat :", output)
