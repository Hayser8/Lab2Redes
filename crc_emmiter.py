#!/usr/bin/env python3
import sys

# Polinomio estándar CRC‑32 (grado 32)
CRC32_POLY = 0x104C11DB7

def crc32_remainder(bitstr: str) -> int:
    """
    Dado un string de bits, devuelve el resto (32 bits) de la división
    polinómica (bit‑a‑bit) tras hacer padding de 32 ceros.
    """
    data = int(bitstr, 2) << 32
    total_bits = len(bitstr) + 32
    for bit in range(total_bits - 1, 31, -1):
        if (data >> bit) & 1:
            data ^= CRC32_POLY << (bit - 32)
    return data & 0xFFFFFFFF

def encode_crc32(bitstr: str) -> str:
    rem = crc32_remainder(bitstr)
    # Resto en binario, 32 bits con ceros a la izquierda
    rem_bits = format(rem, '032b')
    return bitstr + rem_bits

if __name__ == '__main__':
    trama = input('Ingrese la trama de bits (ej. 110101): ').strip()
    # Validación básica
    if not all(c in '01' for c in trama):
        print('Error: solo bits 0 o 1.')
        sys.exit(1)

    codificada = encode_crc32(trama)
    print('Trama codificada con CRC‑32:')
    print(codificada)
