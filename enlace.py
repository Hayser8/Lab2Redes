def hamming_encode(data_bits: str) -> str:
    m = len(data_bits)
    # 1) Calcula r
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    n = m + r
    # 2) Arreglo 1‑indexed
    code = ['0'] * (n + 1)
    # 3) Inserta datos
    j = 0
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            code[i] = data_bits[j]
            j += 1
    # 4) Calcula bits de paridad
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for k in range(1, n + 1):
            if (k & parity_pos) != 0 and k != parity_pos:
                parity ^= int(code[k])
        code[parity_pos] = str(parity)
    return ''.join(code[1:])
