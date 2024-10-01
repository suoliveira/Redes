from socket import *
import sys  

HOST = ''
PORT = 5000
serverSocket = socket(AF_INET, SOCK_STREAM)
origin = (HOST, PORT)

serverSocket.bind(origin)  # Vincular o socket ao endereço IP e porta
serverSocket.listen(1)  
print(f'Servidor está rodando na porta {PORT}...')

while True:
    connectionSocket, client = serverSocket.accept()  # Aceita a conexão
    
    try:
        message = connectionSocket.recv(1024).decode("utf-8")  # Recebe a mensagem do cliente

        if not message:
            print("Nenhuma mensagem recebida.")
            connectionSocket.close()
            continue
        
        lines = message.splitlines()
        filename = lines[0]  
        print(f"Arquivo solicitado: {filename}")
        
        # Extrair o nome do arquivo corretamente
        filename = filename.split()[1] 
        if filename == '/':
            filename = 'HelloWorld.html'
        filename = filename.lstrip("/")  
        f = open(filename)  # Abrir o arquivo solicitado no sistema de arquivos do servidor
        outputdata = f.read()  # Ler o conteúdo do arquivo

        # Enviar uma linha de cabeçalho HTTP para o socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

        # Enviar o conteúdo do arquivo solicitado ao cliente
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())

        # Fechar a conexão com o cliente
        connectionSocket.close()

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # Fechar a conexão com o cliente
        connectionSocket.close()

# Encerrar o servidor
serverSocket.close()
sys.exit()  # Fechar o programa
