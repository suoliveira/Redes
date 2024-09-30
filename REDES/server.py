# Importar o módulo socket
from socket import *
import sys  # Para encerrar o programa

# Criar o socket do servidor
serverSocket = socket(AF_INET, SOCK_STREAM)

# Preparar o socket do servidor
serverPort = 6789  # Porta onde o servidor irá escutar
serverSocket.bind(('', serverPort))  # Vincular o socket ao endereço IP e porta
serverSocket.listen(1)  # Servidor ouvindo conexões TCP, até 1 conexão simultânea
print(f'Servidor está rodando na porta {serverPort}...')

while True:
    # Estabelecer a conexão
    print('Pronto para servir...')
    connectionSocket, addr = serverSocket.accept()  # Aceita a conexão

    try:
        # Receber a mensagem do cliente
        message = connectionSocket.recv(1024).decode()  # Recebe a mensagem do cliente
        filename = message.split()[1]  # O nome do arquivo solicitado
        f = open(filename[1:])  # Abrir o arquivo solicitado no sistema de arquivos do servidor
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
        # Se o arquivo não for encontrado, retornar um erro 404
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # Fechar a conexão com o cliente
        connectionSocket.close()

# Encerrar o servidor
serverSocket.close()
sys.exit()  # Fechar o programa
