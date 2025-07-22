def hamming_encode(data_bits: str) -> str:
    m = len(data_bits)
    # Calcular número de bits de paridad r tal que 2^r >= m + r + 1
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    n = m + r
    # Array 1‑indexed para facilidad
    code = ['0'] * (n + 1)
    # Colocar bits de datos en las posiciones que no sean potencias de 2
    j = 0
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            code[i] = data_bits[j]
            j += 1
    # Calcular cada bit de paridad
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        # XOR de todos los bits cuyo índice tiene el bit i a 1 (excluyendo la propia posición de paridad)
        for k in range(1, n + 1):
            if (k & parity_pos) != 0 and k != parity_pos:
                parity ^= int(code[k])
        code[parity_pos] = str(parity)
    # Devolver la cadena sin el índice 0
    return ''.join(code[1:])

if __name__ == '__main__':
    data = input('Ingrese la trama original en binario (ej. 1011001): ').strip()
    encoded = hamming_encode(data)
    print('Trama codificada (Hamming):', encoded)
