def codificar_mensaje(texto: str) -> str:
    """ ASCII de 8 bits por carácter, concatenados """
    return "".join(f"{ord(c):08b}" for c in texto)

def decodificar_mensaje(bits: str) -> str:
    """ Para el receptor: bits→texto """
    chars = [bits[i : i+8] for i in range(0, len(bits), 8)]
    return "".join(chr(int(b, 2)) for b in chars)
