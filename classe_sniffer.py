''' - cada mac (unico) sniffado deve ser arquivado
    - Se o mac demora mais de 120s sem ser detectado o mac deve ser arquivado
            com a data e hora da primeira e ultima detecção

    Estrutura do codigo:

    * verificar se o mac recebido pertence a uma lista de macs desejados
    * detectar o tempo decorrido entre duas detecções de um mesmo macs
    * salvar banco de dados

'''

from datetime import datetime
import csv

class sniffer:
    def __init__(self, ListaMac):
        self.lista_mac = ListaMac
        self.struct_mac = {}  # {'mac': {primeira_deteccao, ultima_deteccao}}
        self.mac_valido = False
        self.mac = None
        self.cof_espera = 120

    def set_mac(self, endereco):
        self.mac = endereco
        self.status_mac()
        if self.mac_valido == True:
            self.dict_mac()
            self.delta_deteccao()

    def status_mac(self):
        for el_lista_mac in self.lista_mac:
            if self.mac in el_lista_mac:
                self.mac_valido = True
                print('MAC = {} foi detectado!'.format(self.mac))
            else:
                self.mac_valido = False

    def dict_mac(self):
        if self.mac not in self.struct_mac or self.struct_mac[self.mac]['one_detect'] == None:
            self.struct_mac[self.mac] = {'one_detect':datetime.now(),
                            'two_detect':None}
            print('novo mac add')
        else:
            self.struct_mac[self.mac]['two_detect'] = datetime.now()
            print('este mac ja passo por aqui')


    def delta_deteccao(self):
        if self.struct_mac[self.mac]['two_detect'] != None:
            delta_time = self.struct_mac[self.mac]['two_detect'] - self.struct_mac[self.mac]['one_detect']
            if delta_time.seconds > self.cof_espera:
                self.save_mac(self.struct_mac[self.mac])
                print('O MAC: {} foi salvo'.format(self.mac))
                self.struct_mac[self.mac]['one_detect'] = None
                self.struct_mac[self.mac]['two_detect'] = None
            else:
                print('espere mais um pouco')

    def save_mac(self, new_line):
        with open('banco_dados.csv', 'a') as bd:
            linha = csv.writer(bd)
            linha.writerow([self.mac, new_line['one_detect'], new_line['two_detect']])
