from socket import *
import ssl
import base64

# Configuração do servidor
mailserver = ("smtp.gmail.com", 587)  # Gmail SMTP e porta para TLS

def send_command(client_socket, command):
    client_socket.send(command.encode("utf-8"))
    # return client_socket.recv(1024).decode("utf-8")
    recv = client_socket.recv(1024).decode('utf-8')
    print(command)
    print(recv)

# Configuração do e-mail e destinatário
from_email = "seuemail" 
to_email = "seuemail"  
password = "suasenha"  

# Conectar ao servidor com TLS
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024).decode("utf-8")

# Início da conexão segura (STARTTLS)
send_command(clientSocket, "HELO Alice\r\n")
send_command(clientSocket,"STARTTLS\r\n")

# Envolver o socket em SSL
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver[0])
# Autenticação
send_command(clientSocket,"AUTH LOGIN\r\n")

send_command(clientSocket, base64.b64encode(from_email.encode()).decode() +"\r\n")
send_command(clientSocket, base64.b64encode(password.encode()).decode() +"\r\n")

# Enviar comando MAIL FROM e RCPT TO
send_command(clientSocket,"MAIL FROM:<"+from_email+">\r\n")
send_command(clientSocket,"RCPT TO:<"+to_email+">\r\n")

# Configuração da mensagem com imagem em Base64
msg = "Subject: Teste com Imagem\r\n"
msg += "MIME-Version: 1.0\r\n"
msg += "Content-Type: multipart/mixed; boundary=boundary42\r\n\r\n"
msg += "--boundary42\r\n"
msg += "Content-Type: text/plain\r\n\r\n"
msg += "Eu amo redes de computadores!\r\n\r\n"
msg += "--boundary42\r\n"
msg += "Content-Type: image/jpeg\r\n"
msg += "Content-Transfer-Encoding: base64\r\n"
msg += "Content-Disposition: attachment; filename=\"imagem.webp\"\r\n\r\n"

# Abrir imagem e codificar em base64
with open("imagem.webp", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")
msg += image_data + "\r\n"
msg += "--boundary42--\r\n"  # Final do corpo da mensagem

# Comando DATA e envio da mensagem com imagem
send_command(clientSocket, "DATA\r\n")
clientSocket.send(msg.encode("utf-8"))  # Enviar corpo da mensagem com a imagem
send_command(clientSocket, ".\r\n")  # Finalizar o comando DATA

# Comando QUIT
send_command(clientSocket, "QUIT\r\n")

# Fechar a conexão
clientSocket.close()
