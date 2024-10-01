from socket import *

host = input("Digite o endereço: ")
port = int(input("Digite a porta: "))
filename = input("Digite o nome do arquivo: ")

socket = socket(AF_INET, SOCK_STREAM)
socket.connect((host, port))

request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"

socket.send(request.encode())

response = socket.recv(1024).decode("utf-8")
print(response)

socket.close()
