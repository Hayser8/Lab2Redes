import random

def aplicar_ruido(bits: str, tasa_error: float) -> str:
    return ''.join(
        ('1' if b=='0' else '0') if random.random()<tasa_error else b
        for b in bits
    )