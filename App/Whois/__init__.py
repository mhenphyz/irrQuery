import socket
from .as_set import *
from pprint import pprint
from re import match
from time import sleep

class Whois:
    
    def __init__(self, as_set_name: str, all_as_sets:list ,server: str = 'whois.radb.net', port: int = 43, timeout: int = 10) -> None:
        self.name = as_set_name
        self.server = server
        self.port = port
        self.timeout = timeout
        self.connection = None
        self.as_set = self.get_as_set(as_set_name)
        self.sets = all_as_sets
        self.origins = self.get_origins(*self.as_set['members']) if self.as_set is not None else None
        
    def __connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.timeout)
        self.connection.connect((self.server, self.port))
        
    def __send_query(self, query: str) -> str:
        print(query)
        self.connection.send(query.encode())
        
        response = ''
        
        while True:
            data = self.connection.recv(4096).decode()
            response += data

            if not data: break
            
        return response
        
        
    def get_as_set(self, as_set_name: str) -> None:
        # inicia conexao com servidor whois
        try:
            self.__connect()

            # faz a consulta do objeto as-set  e fecha a sessao
            query = ' -T as-set {0}{1}'.format(as_set_name, "\r\n")
            response = self.__send_query(query)

            #TODO log everything not found
            if match('.*No entries found.*', response):
                return None

            self.connection.close()
        except ConnectionResetError:
            sleep(5)
            self.__connect()

            # faz a consulta do objeto as-set  e fecha a sessao
            query = ' -T as-set {0}{1}'.format(as_set_name, "\r\n")
            response = self.__send_query(query)

            #TODO log everything not found
            if match('.*No entries found.*', response):
                return None

            self.connection.close()
        
        # converte objeto as-set de string para um objeto
        # esse metodo tambem fara a separacao de origens e as-set
        data = as_set_to_dict(response)
        return data
    
    def get_origins(self, origins: list, as_sets: list,):
        
        for as_set_member in as_sets:

            if as_set_member in self.sets: continue
            
            self.sets.append(as_set_member)
                
            member_set = Whois(as_set_member, self.sets)            
            origins.append(member_set.origins)
            print(f"{self.name} ===================================== {self.sets}")
        
        return origins
        