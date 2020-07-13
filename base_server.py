from socket import *
import time
from classe_sniffer import sniffer as sf



lista_mac = ['0a9838fa20c3','a450467abe5b']

meuHost = ''

minhaPort = 5000

sockobj = socket(AF_INET, SOCK_STREAM)

sockobj.bind(('192.168.0.8', minhaPort))

sockobj.listen(5)

sniffer = sf(lista_mac)



while True:
	conexao, endereco = sockobj.accept()

	while True:
		# Recebe data enviada pelo cliente
		data = conexao.recv(1024)
		data_decode = data.decode('utf-8')

		# Se não receber nada paramos o loop
		if not data:
			break
		else:
#			print(data_decode[:10])
			sniffer.set_mac(data_decode[:10], data_decode[11:])
			sniffer.delta_deteccao()

	conexao.close()
