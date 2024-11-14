import socket
from nsip import *

# definindo o IP do servidor
IP = "127.0.0.1"

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# criando um pacote de requisição NSIP
req_packet = NSIPPacket(id=1, type=NSIP_REQ, query=SYS_PROCNUM, result="")
req_packet.checksum = checksum(req_packet.to_packet())
print("Pacote de requisição:")
req_packet.print()

# enviando o pacote de requisição para o servidor
s.sendto(req_packet.to_packet(), (IP, PORTANUMERO))

# recebendo o pacote de resposta do servidor
buffer, server_address = s.recvfrom(500)

# convertendo o pacote recebido em um objeto NSIPPacket
response_packet = NSIPPacket()
response_packet.from_packet(buffer)

#Imprimindo o pacote
print("Pacote recebido do servidor:")
response_packet.print()

# fechando o socket
s.close()