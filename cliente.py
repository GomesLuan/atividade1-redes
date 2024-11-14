import socket
from nsip import *

# definindo o IP do servidor
IP = "127.0.0.1"

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# criando um pacote de requisição NSIP
packet = NSIPPacket(id=1, type=NSIP_REQ, query=SYS_BOOTIME, result="")
packet.checksum = checksum(packet.to_packet())
print("Pacote de requisição:")
packet.print()

# enviando o pacote de requisição para o servidor
s.sendto(packet.to_packet(), (IP, PORTANUMERO))

# recebendo o pacote de resposta do servidor
buffer, server_address = s.recvfrom(500)

# convertendo o pacote recebido em um objeto NSIPPacket
packet.from_packet(buffer)

# Verificação através do checksum
original_checksum = packet.checksum
recalculated_checksum = checksum(packet.to_packet())
if recalculated_checksum != original_checksum:
    packet.type = NSIP_ERR
    packet.result = "Checksum inválido"

#Imprimindo o pacote
print("Pacote recebido do servidor:")
packet.print()

# fechando o socket
s.close()