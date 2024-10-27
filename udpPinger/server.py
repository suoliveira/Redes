import random
from socket import *

# Criação do socket UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Atribuir endereço IP e número da porta ao socket
serverSocket.bind(('localhost', 12000))
print(f"Servidor rodando em {'localhost'} {12000}")

while True:
    # Gera um número aleatório entre 0 e 10 para simular perda de pacotes
    rand = random.randint(0, 10)
    
    # Recebe o pacote do cliente e o endereço de origem
    message, address = serverSocket.recvfrom(1024)
    
    # Converte a mensagem recebida para letras maiúsculas
    message = message.upper()
    
    # Se o número rand for menor que 4, simula a perda do pacote
    if rand < 4:
        continue
    
    # Envia a mensagem de volta ao cliente (echo), convertida de volta para bytes
    serverSocket.sendto(message, address)
