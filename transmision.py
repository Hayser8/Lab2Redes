import socket

def enviar_trama(trama: str, host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(trama.encode('utf-8'))
