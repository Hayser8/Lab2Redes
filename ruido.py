import random

def aplicar_ruido(bits: str, tasa_error: float) -> str:
    """
    Invierte cada bit con probabilidad `tasa_error`.
    """
    result = []
    for b in bits:
        if random.random() < tasa_error:
            result.append('1' if b == '0' else '0')
        else:
            result.append(b)
    return ''.join(result)
