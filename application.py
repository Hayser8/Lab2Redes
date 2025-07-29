def solicitar_mensaje():
    texto = input("Escribe el mensaje a enviar: ")
    tasa_error = float(input("Tasa de error (p.ej. 0.01 para 1%): "))
    host = input("Host receptor (p.ej. localhost): ")
    port = int(input("Puerto receptor (p.ej. 5001): "))
    return texto, tasa_error, host, port

def mostrar_trama_local(trama: str):
    print("\n---- Trama FINAL (con ruido) ----")
    print(trama)