from socket import *
import sys

HOST = "127.0.0.1"
PORT = 8888

def get_content_type(filename):
    if filename.endswith('.html'):
        return "text/html"
    elif filename.endswith(('.jpg', '.jpeg')):
        return "image/jpeg"
    return "application/octet-stream"

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen(1)

try:
    while True:
        print('Pronto para servir...')
        tcpCliSock, addr = tcpSerSock.accept()
        message = tcpCliSock.recv(1024).decode('utf-8', 'ignore')
        
        try:
            filename = message.split()[1][1:]  # Remove o leading '/'
            print("Arquivo solicitado:", filename)

            try:
                with open(filename, "rb") as f:
                    outputdata = f.read()
                    print("Lido do cache.")
                    
                    tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
                    tcpCliSock.send(f"Content-Type:{get_content_type(filename)}\r\n\r\n".encode())
                    tcpCliSock.send(outputdata)
            except IOError:
                hostn = filename.replace("www.", "", 1)
                print("Servidor remoto:", hostn)
                
                try:
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((hostn, 80))
                    c.sendall(f"GET / HTTP/1.1\r\nHost: {hostn}\r\nConnection: close\r\n\r\n".encode('utf-8'))
                    
                    with open(filename, "wb") as tmpFile:
                        while True:
                            buff = c.recv(4096)
                            if not buff:
                                break
                            tmpFile.write(buff)
                            tcpCliSock.send(buff)
                    c.close()
                except Exception as e:
                    print("Erro ao conectar ao servidor remoto:", e)
                    tcpCliSock.send("HTTP/1.1 404 Not Found\r\n".encode())
                    tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
                    tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
                    
        except IndexError:
            print("Solicitação HTTP inválida")
            tcpCliSock.send("HTTP/1.1 400 Bad Request\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send("<html><body><h1>400 Bad Request</h1></body></html>".encode())
        
        tcpCliSock.close()
except KeyboardInterrupt:
    print("Servidor encerrado.")
    tcpSerSock.close()
    sys.exit()

