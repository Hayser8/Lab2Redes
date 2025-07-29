def _hamming_encode_block(data_bits: str) -> str:
    """
    Extendido Hamming(12,8): para m=8 calcula r=4 y devuelve 12 bits.
    """
    # pre: len(data_bits)==8
    m = 8
    r = 4
    n = m + r  # 12
    code = ['0'] * (n + 1)
    # coloca datos en posiciones no potencias de 2
    j = 0
    for i in range(1, n + 1):
        if (i & (i-1)) != 0:
            code[i] = data_bits[j]
            j += 1
    # calcula bits de paridad en posiciones 1,2,4,8
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for k in range(1, n + 1):
            if (k & parity_pos) != 0 and k != parity_pos:
                parity ^= int(code[k])
        code[parity_pos] = str(parity)
    return ''.join(code[1:])


def hamming_encode_message(bits: str) -> str:
    """
    Divide en bloques de 8 bits y aplica _hamming_encode_block a cada uno.
    """
    bloques = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return "".join(_hamming_encode_block(b) for b in bloques)
