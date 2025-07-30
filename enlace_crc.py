# enlace.py

import zlib

def calcular_integridad(bits: str) -> str:
    """
    Calcula CRC‑32 sobre los bytes originales y concatena los 32 bits de CRC al final.
    """
    # Agrupa los bits en bytes
    n_bytes = len(bits) // 8
    data = int(bits, 2).to_bytes(n_bytes, byteorder='big')
    crc = zlib.crc32(data) & 0xFFFFFFFF
    crc_bits = f"{crc:032b}"
    return bits + crc_bits

def verificar_integridad(trama: str) -> bool:
    """
    Separa datos y CRC, recalcula y compara.
    Devuelve True si coincide, False si hay error.
    """
    data_bits = trama[:-32]
    crc_bits  = trama[-32:]
    n_bytes = len(data_bits) // 8
    data = int(data_bits, 2).to_bytes(n_bytes, byteorder='big')
    calc_crc = zlib.crc32(data) & 0xFFFFFFFF
    return crc_bits == f"{calc_crc:032b}"
