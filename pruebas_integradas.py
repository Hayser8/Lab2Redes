import subprocess
import socket
import time
import os
import random

import numpy as np
import matplotlib.pyplot as plt

from presentation import codificar_mensaje
from enlace import hamming_encode_message
from ruido import aplicar_ruido

# ——— Protección por Paridad Simple ———
def encode_parity(bits: str) -> str:
    """Añade un bit de paridad par al final."""
    parity = bits.count('1') % 2
    return bits + str(parity)

def decode_parity(trama: str):
    """Devuelve (datos, correcto:bool) tras verificar paridad."""
    data, p = trama[:-1], trama[-1]
    ok = (data.count('1') % 2) == int(p)
    return data, ok

# ——— Hamming decode local para métricas ———
def _hamming_decode_block(c: str):
    n, r = 12, 4
    err = 0
    for i in range(r):
        p = 2**i; total = 0; j = p-1
        while j < n:
            total += c[j:j+p].count('1')
            j += 2*p
        if total % 2: err += p
    arr = list(c); corr = 0
    if 1 <= err <= n:
        idx = err-1
        arr[idx] = '1' if arr[idx]=='0' else '0'
        corr = 1
    data = "".join(arr[i] for i in range(n) if ((i+1)&i)!=0)
    diff = sum(a!=b for a,b in zip(c, ''.join(arr)))
    uncorr = 1 if diff>corr else 0
    return data, corr, uncorr

def hamming_decode(bits: str):
    bloques = [bits[i:i+12] for i in range(0, len(bits), 12)]
    data=""; tot_corr=tot_unc=0
    for b in bloques:
        d,c,u = _hamming_decode_block(b)
        data+=d; tot_corr+=c; tot_unc+=u
    return data, tot_corr, tot_unc

# ——— Orquestación Node.js ———
def start_receptor_node(port: int):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receptor_script = os.path.join(script_dir, "receptor", "receptor.js")
    proc = subprocess.Popen(
        ["node", receptor_script, str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding='utf-8', errors='ignore'
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("El receptor no arrancó.")
        if "escuchando" in line.lower():
            break
    return proc

def send_trama(trama: str, host: str, port: int):
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall(trama.encode())
        time.sleep(0.01)

def receive_decoded(proc):
    decoded = None
    while True:
        line = proc.stdout.readline()
        if not line: break
        if line.strip().startswith("---- MENSAJE DECODIFICADO"):
            decoded = proc.stdout.readline().strip()
            break
    return decoded

# ——— Métricas ———
def metric_success_vs_length(lengths, ber, trials):
    rates = []
    for L in lengths:
        succ = 0
        for _ in range(trials):
            msg = "A"*L
            bits = codificar_mensaje(msg)
            enc = hamming_encode_message(bits)
            noisy = aplicar_ruido(enc, ber)
            dec_bits, _, _ = hamming_decode(noisy)
            rec = "".join(chr(int(dec_bits[i:i+8],2)) for i in range(0,len(dec_bits),8))
            if rec == msg: succ += 1
        rates.append(succ/trials)
    return rates

def metric_corrections_vs_ber(noise_levels, trials):
    avg = []
    for p in noise_levels:
        csum=0; blocks=0
        for _ in range(trials):
            bits = codificar_mensaje("A"*20)
            enc = hamming_encode_message(bits)
            noisy = aplicar_ruido(enc, p)
            _, c, _ = hamming_decode(noisy)
            csum += c
            blocks += len(bits)//8
        avg.append(csum/blocks)
    return avg

def metric_per_vs_ber(noise_levels):
    return [1 - ((1-p)**12 + 12*p*(1-p)**11) for p in noise_levels]

def metric_compare_schemes(noise_levels, msg, trials):
    bits = codificar_mensaje(msg)
    raw = []; par = []; ham = []
    for p in noise_levels:
        sr=sp=sh=0
        for _ in range(trials):
            # Raw
            if aplicar_ruido(bits,p) == bits: sr += 1
            # Parity
            encp = encode_parity(bits)
            dp, ok = decode_parity(aplicar_ruido(encp,p))
            if ok and "".join(chr(int(dp[i:i+8],2)) for i in range(0,len(dp),8))==msg: sp+=1
            # Hamming
            enh = hamming_encode_message(bits)
            dh, _, _ = hamming_decode(aplicar_ruido(enh,p))
            if "".join(chr(int(dh[i:i+8],2)) for i in range(0,len(dh),8))==msg: sh+=1
        raw.append(sr/trials); par.append(sp/trials); ham.append(sh/trials)
    return {"Raw":raw, "Parity":par, "Hamming":ham}

def metric_latency_vs_ber(noise_levels):
    return [1/((1-p)**12 + 12*p*(1-p)**11) for p in noise_levels]

def metric_integrated(message, noise_levels, trials, host, port):
    proc = start_receptor_node(port)
    time.sleep(0.1)
    rates = []
    for p in noise_levels:
        succ = 0
        for _ in range(trials):
            bits = codificar_mensaje(message)
            enc = hamming_encode_message(bits)
            noisy = aplicar_ruido(enc, p)
            send_trama(noisy, host, port)
            if receive_decoded(proc) == message:
                succ += 1
        rates.append(succ/trials)
    proc.terminate()
    return rates

# ——— Main y Plots ———
if __name__ == "__main__":
    HOST, PORT = "localhost", 5001
    MESSAGE    = "hola como estas"
    LENGTHS    = [5, 10, 20, 50]
    BERS_FIXED = [0.01, 0.05, 0.10]
    NOISE_L    = np.arange(0, 0.101, 0.005)
    TRIALS     = 200

    # 0) Integrado
    r0 = metric_integrated(MESSAGE, NOISE_L, TRIALS, HOST, PORT)
    plt.figure(); plt.plot(NOISE_L*100, r0, 'o-')
    plt.title("Integrado: Éxito vs BER"); plt.xlabel("BER (%)"); plt.ylabel("Frac."); plt.grid(True); plt.show()

    # 1) Éxito vs Longitud
    plt.figure()
    for ber in BERS_FIXED:
        r1 = metric_success_vs_length(LENGTHS, ber, TRIALS)
        plt.plot(LENGTHS, r1, 'o-', label=f'{ber*100:.0f}%')
    plt.title("Éxito vs Longitud"); plt.xlabel("Len"); plt.ylabel("Frac."); plt.legend(); plt.grid(True); plt.show()

    # 2) Correcciones vs BER
    r2 = metric_corrections_vs_ber(NOISE_L, TRIALS)
    plt.figure(); plt.plot(NOISE_L*100, r2, 'o-')
    plt.title("Correcciones/bloque vs BER"); plt.xlabel("BER (%)"); plt.ylabel("Promedio"); plt.grid(True); plt.show()

    # 3) PER vs BER
    r3 = metric_per_vs_ber(NOISE_L)
    plt.figure(); plt.plot(NOISE_L*100, r3, 'o-')
    plt.title("PER vs BER"); plt.xlabel("BER (%)"); plt.ylabel("PER"); plt.grid(True); plt.show()

    # 4) Comparativa esquemas
    cmp = metric_compare_schemes(NOISE_L, "A"*15, TRIALS)
    plt.figure()
    for k,v in cmp.items():
        plt.plot(NOISE_L*100, v, 'o-', label=k)
    plt.title("Comparativa"); plt.xlabel("BER (%)"); plt.ylabel("Frac."); plt.legend(); plt.grid(True); plt.show()

    # 5) Retransmisiones vs BER
    r5 = metric_latency_vs_ber(NOISE_L)
    plt.figure(); plt.plot(NOISE_L*100, r5, 'o-')
    plt.title("Tx promedio vs BER"); plt.xlabel("BER (%)"); plt.ylabel("Tx"); plt.grid(True); plt.show()
