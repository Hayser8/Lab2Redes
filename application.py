def solicitar_mensaje():
    texto = input("Escribe el mensaje a enviar: ")
    tasa_error = float(input("Tasa de error (p.ej. 0.01 para 1%): "))
    return texto, tasa_error

def mostrar_trama(trama: str):
    print("\n---- Trama FINAL (con ruido) ----")
    print(trama)
