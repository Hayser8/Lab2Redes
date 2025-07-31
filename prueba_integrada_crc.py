import os
import subprocess
import socket
import time
import random
import zlib

import numpy as np
import matplotlib.pyplot as plt

from presentation import codificar_mensaje
from ruido import aplicar_ruido

# --- CRC-32 Encoding and Verification ---

def calcular_integridad_crc(bits: str) -> str:
    n_bytes = len(bits) // 8
    data = int(bits, 2).to_bytes(n_bytes, byteorder="big")
    crc = zlib.crc32(data) & 0xFFFFFFFF
    return bits + f"{crc:032b}"

def verificar_integridad_crc(trama: str) -> bool:
    data_bits = trama[:-32]
    crc_bits  = trama[-32:]
    n_bytes = len(data_bits) // 8
    data = int(data_bits, 2).to_bytes(n_bytes, byteorder="big")
    calc_crc = zlib.crc32(data) & 0xFFFFFFFF
    return crc_bits == f"{calc_crc:032b}"

# --- TCP Utilities ---

def start_receptor_crc(port: int):
    folder = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(folder, "receptor", "receptorcrc.js")
    proc = subprocess.Popen(
        ["node", script, str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="ignore"
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("El receptor CRC no arrancó.")
        if "escuchando" in line.lower():
            break
    return proc

def send_trama(trama: str, host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(trama.encode("utf-8"))
        time.sleep(0.01)

def receive_outcome(proc):
    success = False
    detected = False
    while True:
        out = proc.stdout.readline()
        if not out:
            break
        if out.strip().startswith("---- MENSAJE DECODIFICADO"):
            _ = proc.stdout.readline()
            success = True
            break
        if "error de integridad" in out.lower():
            detected = True
            break
    return success, detected

# --- Metrics ---

def metric_integrated_crc(message, noise_levels, trials, host, port):
    proc = start_receptor_crc(port)
    time.sleep(0.1)
    succs, dets, unds = [], [], []
    bits = codificar_mensaje(message)
    frame = calcular_integridad_crc(bits)
    for p in noise_levels:
        s = d = u = 0
        for _ in range(trials):
            noisy = aplicar_ruido(frame, p)
            send_trama(noisy, host, port)
            ok, det = receive_outcome(proc)
            if ok:
                s += 1
            elif det:
                d += 1
            else:
                u += 1
        succs.append(s/trials)
        dets.append(d/trials)
        unds.append(u/trials)
        print(f"BER={p*100:.2f}% → succ={s/trials:.3f}, det={d/trials:.3f}, und={u/trials:.3f}")
    proc.terminate()
    return succs, dets, unds

def metric_success_vs_length_crc(lengths, ber, trials):
    rates = []
    for L in lengths:
        s = 0
        for _ in range(trials):
            msg = "A"*L
            bits = codificar_mensaje(msg)
            frame = calcular_integridad_crc(bits)
            noisy = aplicar_ruido(frame, ber)
            if verificar_integridad_crc(noisy):
                s += 1
        rates.append(s/trials)
    return rates

def metric_theoretical_detection(noise_levels, frame_bits):
    return [1 - (1-p)**frame_bits for p in noise_levels]

if __name__ == "__main__":
    HOST, PORT = "localhost", 5003
    MESSAGE = "hola como estas"
    NOISE_LEVELS = np.arange(0, 0.0201, 0.001)  # 0–2% en pasos de 0.1%
    TRIALS = 500

    bitlen = len(codificar_mensaje(MESSAGE)) + 32
    overhead = 32/bitlen*100
    print(f"Overhead CRC-32: {overhead:.1f}%")

    # Integrated
    succ, det, und = metric_integrated_crc(MESSAGE, NOISE_LEVELS, TRIALS, HOST, PORT)
    theo = metric_theoretical_detection(NOISE_LEVELS, bitlen)

    plt.figure()
    plt.plot(NOISE_LEVELS*100, succ, 'o-', label="Success")
    plt.plot(NOISE_LEVELS*100, det, 's-', label="Detected")
    plt.plot(NOISE_LEVELS*100, und, 'x-', label="Undetected")
    plt.plot(NOISE_LEVELS*100, theo, 'k--', label="Teórico detect")
    plt.title("CRC-32: Success/Detected/Undetected vs BER")
    plt.xlabel("BER (%)"); plt.ylabel("Frac."); plt.legend(); plt.grid(True); plt.tight_layout(); plt.show()

    # Success vs Length
    LENGTHS = [5, 10, 20, 50]
    BERS_FIXED = [0.01, 0.05, 0.10]
    plt.figure()
    for ber in BERS_FIXED:
        rates = metric_success_vs_length_crc(LENGTHS, ber, TRIALS)
        plt.plot(LENGTHS, rates, 'o-', label=f"{ber*100:.0f}% BER")
    plt.title("CRC-32: Éxito vs Longitud")
    plt.xlabel("Longitud (caracteres)"); plt.ylabel("Frac. pasaron CRC"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.show()
