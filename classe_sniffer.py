''' - cada mac (unico) sniffado deve ser arquivado
    - Se o mac demora mais de 120s sem ser detectado o mac deve ser arquivado
            com a data e hora da primeira e ultima detecção

    Estrutura do codigo:

    * verificar se o mac recebido pertence a uma lista de macs desejados
    * detectar o tempo decorrido entre duas detecções de um mesmo macs
    * salvar banco de dados

'''
from threading import Thread
from datetime import datetime
import csv

class sniffer:
    def __init__(self, ListaMac):
        self.lista_mac = ListaMac
        self.struct_mac = {}  # {'mac': {primeira_deteccao, ultima_deteccao}}
        self.mac_valido = False
        self.mac = None
        self.db = None
        self.cof_espera = 10


    def set_mac(self, endereco, intensidade):
        self.mac = endereco
        self.status_mac()
        if self.mac_valido == True:
            self.set_db(intensidade)
            self.dict_mac()
        self.mac_valido = False

    def set_db(self, intensity):
        self.db = intensity

    def status_mac(self):
        for el_lista_mac in self.lista_mac:
            if self.mac in el_lista_mac:
                self.mac_valido = True
                print('MAC = {} DB = {} foi detectado!'.format(self.mac, self.db))

    def dict_mac(self):
        if self.mac not in self.struct_mac:
            self.struct_mac[self.mac] = {'mac':self.mac,
                                        'one_detect':datetime.now(),
                                        'one_detect_db':self.db,
                                        'two_detect': None,
                                        'two_detect_db':None}
            print('novo mac add')
        else:
            self.struct_mac[self.mac]['two_detect'] = datetime.now()
            self.struct_mac[self.mac]['two_detect_db'] = self.db
            print('este mac ja passo por aqui')


    def deley_two_detect(self, mac):
        delay = datetime.now() - self.struct_mac[mac]['one_detect']
        if delay.seconds > self.cof_espera:
            return True
        else:
            return False

    def delta_deteccao(self):
        for mac in list(self.struct_mac.keys()):
            if self.struct_mac[mac]['two_detect'] != None:
                date_time = datetime.now() - self.struct_mac[mac]['two_detect']
                if date_time.seconds > self.cof_espera:
                    print('mac salvo')
                    self.save_mac(self.struct_mac[mac])
                    del self.struct_mac[mac]
            else:
                if self.deley_two_detect(mac):
                    print('mac salvo sem two_detect')
                    self.save_mac(self.struct_mac[mac])
                    del self.struct_mac[mac]


    def save_mac(self, new_line):
        with open('banco_dados.csv', 'a') as bd:
            linha = csv.writer(bd)
            linha.writerow([new_line['mac'], new_line['one_detect'],new_line['one_detect_db'], new_line['two_detect'],new_line['two_detect_db']])
