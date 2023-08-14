def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    alphabet_len = 26
    ciphertext = ""

    for i in range(len(plaintext)):
        l = plaintext[i]
        if l.isalpha():
            shift = ord(keyword[i % len(keyword)].lower()) - ord("a")
            pivot = ord("a" if l.islower() else "A")
            char_shift = (ord(l) - pivot + shift) % alphabet_len
            ciphertext += chr(char_shift + pivot)
        else:
            ciphertext += l

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    alphabet_len = 26
    plaintext = ""

    for i in range(len(ciphertext)):
        l = ciphertext[i]
        if l.isalpha():
            shift = -(ord(keyword[i % len(keyword)].lower()) - ord("a"))
            pivot = ord("a" if l.islower() else "A")
            char_shift = (ord(l) - pivot + shift) % alphabet_len
            plaintext += chr(char_shift + pivot)
        else:
            plaintext += l

    return plaintext
