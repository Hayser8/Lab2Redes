from application import solicitar_mensaje, mostrar_trama
from presentation import codificar_mensaje
from enlace import hamming_encode
from ruido import aplicar_ruido

def main():
    # Capa APLICACIÓN
    texto, tasa_error = solicitar_mensaje()

    # Capa PRESENTACIÓN
    bits = codificar_mensaje(texto)
    print("\n---- Bits ASCII ----")
    print(bits)

    # Capa ENLACE
    trama_hamming = hamming_encode(bits)
    print("\n---- Trama con Hamming ----")
    print(trama_hamming)

    # Capa RUIDO
    trama_ruidosa = aplicar_ruido(trama_hamming, tasa_error)
    mostrar_trama(trama_ruidosa)

if __name__ == "__main__":
    main()
