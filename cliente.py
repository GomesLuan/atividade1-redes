# importando o modulo socket
import socket

from nsip import *

# definindo o IP do servidor
IP = "127.0.0.1"

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# enviando a requisição para o servidor
msg = "horaAtual".encode("ISO-8859-1")
s.sendto(msg, (IP, PORTANUMERO))

# recebendo a resposta do servidor
buffer, server_address = s.recvfrom(500)

# imprimindo a hora recebida
print("Hora certa: %s" % buffer.decode("ISO-8859-1"))

# fechando o socket
s.close()