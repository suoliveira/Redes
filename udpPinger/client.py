import time
from socket import *

# Criação do socket UDP do cliente
clientSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('localhost', 12000)
clientSocket.settimeout(1)  # Define o tempo limite de 1 segundo

# Inicialização de variáveis para cálculos de estatísticas
rtt_list = []
timeouts = 0
total_pings = 10

for i in range(1, total_pings + 1):
   
    try: 
        # Criação da mensagem de ping com número de sequência e tempo
        send_time = time.time()

        message = f"Ping {i}"
        # Envia a mensagem para o servidor
        clientSocket.sendto(message.encode(), serverAddress)

        # Espera a resposta do servidor
        response, server = clientSocket.recvfrom(1024)
        receive_time = time.time()
        
        # Cálculo do RTT
        rtt = receive_time - send_time
        rtt_list.append(rtt)

        print(f"Resposta: {response.decode()} | tempo: {((rtt) * 1000):.2f} ms")

    except timeout:
        # Caso o tempo se esgote e não haja resposta
        print("Timeout")
        timeouts += 1

# Estatísticas de RTT
if rtt_list:
    min_rtt = min(rtt_list)
    max_rtt = max(rtt_list)
    avg_rtt = sum(rtt_list) / len(rtt_list)
else:
    min_rtt = max_rtt = avg_rtt = 0

print("\n **********Estatísticas**********")
print(f"RTT mínimo: {min_rtt * 1000:.2f} ms")
print(f"RTT máximo: {max_rtt * 1000:.2f} ms")
print(f"RTT médio: {avg_rtt * 1000:.2f} ms")
print(f"Timeouts: {timeouts} = {timeouts / total_pings * 100:.2f}%")

# Fecha o socket do cliente
clientSocket.close()
