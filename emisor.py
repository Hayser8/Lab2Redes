from application import solicitar_mensaje, mostrar_trama_local
from presentation import codificar_mensaje
from enlace import hamming_encode_message
from ruido import aplicar_ruido
from transmision import enviar_trama

def main():
    # 1) APLICACIÓN
    texto, tasa_error, host, port = solicitar_mensaje()

    # 2) PRESENTACIÓN
    bits = codificar_mensaje(texto)
    print("\n---- Bits ASCII ----")
    print(bits)

    # 3) ENLACE (por carácter)
    trama_hamming = hamming_encode_message(bits)
    print("\n---- Trama con Hamming(12,8) ----")
    print(trama_hamming)

    # 4) RUIDO
    trama_ruidosa = aplicar_ruido(trama_hamming, tasa_error)
    mostrar_trama_local(trama_ruidosa)

    # 5) TRANSMISIÓN
    print(f"\nEnviando trama a {host}:{port} …")
    enviar_trama(trama_ruidosa, host, port)
    print("Envío completado.")

if __name__ == "__main__":
    main()