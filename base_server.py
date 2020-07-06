from socket import *
import time
from classe_sniffer import sniffer as sf



lista_mac = ['0A9838FA20C3','48FDA375B389']

meuHost = ''

minhaPort = 5000

sockobj = socket(AF_INET, SOCK_STREAM)

sockobj.bind(('192.168.0.8', minhaPort))

sockobj.listen(5)

sniffer = sf(lista_mac)

while True:

	conexão, endereço = sockobj.accept()

	while True:
		# Recebe data enviada pelo cliente
		data = conexão.recv(1024)
		data_decode = data.decode('utf-8')

		# Se não receber nada paramos o loop
		if not data:
			break
		else:
			sniffer.set_mac(data_decode[:12])

	conexão.close()
