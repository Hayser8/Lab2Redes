# emisor_crc.py

from application import solicitar_mensaje, mostrar_trama_local
from presentation import codificar_mensaje
from enlace_crc import calcular_integridad
from ruido import aplicar_ruido
from transmision import enviar_trama

def main():
    texto, tasa_error, host, port = solicitar_mensaje()

    bits = codificar_mensaje(texto)
    print("\n---- Bits ASCII ----")
    print(bits)

    trama_crc = calcular_integridad(bits)
    print("\n---- Trama con CRC‑32 ----")
    print(trama_crc)

    trama_ruidosa = aplicar_ruido(trama_crc, tasa_error)
    mostrar_trama_local(trama_ruidosa)

    print(f"\nEnviando trama a {host}:{port} …")
    enviar_trama(trama_ruidosa, host, port)
    print("Envío completado.")

if __name__ == "__main__":
    main()
