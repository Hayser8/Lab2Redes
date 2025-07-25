def codificar_mensaje(texto: str) -> str:
    """
    Convierte cada carácter a ASCII binario de 8 bits y concatena.
    """
    return "".join(f"{ord(c):08b}" for c in texto)

def decodificar_mensaje(bits: str) -> str:
    """
    (No se usa en el emisor, pero sirve en el receptor)
    """
    chars = [bits[i : i+8] for i in range(0, len(bits), 8)]
    return "".join(chr(int(b, 2)) for b in chars)
