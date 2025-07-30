import subprocess
import socket
import time
import random
import os

import numpy as np
import matplotlib.pyplot as plt

# --- Hamming(12,8) helpers (igual que antes) ---

def codificar_mensaje(texto: str) -> str:
    return "".join(f"{ord(c):08b}" for c in texto)

def _hamming_encode_block(data_bits: str) -> str:
    m, r = 8, 4
    n = m + r
    code = ['0'] * (n + 1)
    j = 0
    for i in range(1, n + 1):
        if (i & (i-1)) != 0:
            code[i] = data_bits[j]
            j += 1
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for k in range(1, n + 1):
            if (k & parity_pos) != 0 and k != parity_pos:
                parity ^= int(code[k])
        code[parity_pos] = str(parity)
    return ''.join(code[1:])

def hamming_encode_message(bits: str) -> str:
    bloques = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return "".join(_hamming_encode_block(b) for b in bloques)

def aplicar_ruido(bits: str, tasa_error: float) -> str:
    return ''.join(
        ('1' if b=='0' else '0') if random.random() < tasa_error else b
        for b in bits
    )

# --- Orquestación integrada ---

def start_receptor_node(port: int):
    """
    Arranca receptor.js como servidor Node en segundo plano,
    apuntando a la carpeta receptor/ donde está el script.
    """
    # Ruta absoluta al receptor.js
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receptor_script = os.path.join(script_dir, "receptor", "receptor.js")

    proc = subprocess.Popen(
        ["node", receptor_script, str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    # Espera a la línea de arranque
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("El receptor no arrancó correctamente.")
        if f"Receptor escuchando en puerto {port}" in line:
            break
    return proc

def send_trama(trama: str, host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(trama.encode("utf-8"))
        time.sleep(0.01)

def test_noise_levels_integrated(message: str, noise_levels, trials: int, host: str, port: int):
    receptor_proc = start_receptor_node(port)
    time.sleep(0.1)

    bits = codificar_mensaje(message)
    enc = hamming_encode_message(bits)

    success_rates = []
    for p in noise_levels:
        succ = 0
        for _ in range(trials):
            noisy = aplicar_ruido(enc, p)
            send_trama(noisy, host, port)

            decoded = None
            # Leer hasta encontrar la etiqueta de mensaje
            while True:
                out = receptor_proc.stdout.readline()
                if not out:
                    break
                if out.strip().startswith("---- MENSAJE DECODIFICADO"):
                    decoded = receptor_proc.stdout.readline().strip()
                    break

            if decoded == message:
                succ += 1

        rate = succ / trials
        print(f"Ruido {p:.3f}: {rate*100:.1f}% éxito")
        success_rates.append(rate)

    receptor_proc.terminate()
    return success_rates

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5001
    MESSAGE = "hola como estas"
    NOISE_LEVELS = np.arange(0, 0.101, 0.005)   # 0% a 10% en pasos de 0.5%
    TRIALS = 200

    rates = test_noise_levels_integrated(MESSAGE, NOISE_LEVELS, TRIALS, HOST, PORT)

    plt.plot(NOISE_LEVELS * 100, rates, marker="o")
    plt.title("Éxito de decodificación vs nivel de ruido\n(Integrado Python ↔ Node.js)")
    plt.xlabel("Nivel de ruido (BER %)")
    plt.ylabel("Fracción de mensajes correctos")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
