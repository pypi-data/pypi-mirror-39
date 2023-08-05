# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2018

@author: koliveirab
'''
import http.server
import socketserver
import socket
from Pyautomators.Runner_Pyautomators import orquestrador
from Pyautomators.Dados import pegarConteudoYAML
import shutil,os,re
from distutils.dir_util import copy_tree
''' Esta modulo tem o intuito de trabalhar em conjunto comunica��o entre sistemas e gera��o de Threads, 
trabalhando com cloud, processos e sistemas provedores de servi�os de nuvem e docker'''


def servidor_http(endereco:str,porta:int):
    '''Esta fun��o tem como principio gerar um servidor http'''
    #criando um objeto servidor
    Handler = http.server.SimpleHTTPRequestHandler
    #criando o objeto para servidor socket tcp
    httpd = socketserver.TCPServer((endereco, porta), Handler)
    #subindo o servidor e rodando com while==true
    httpd.serve_forever()
    
class Runner_Master():
    def __init__(self,file_yaml):
        self.file=pegarConteudoYAML(file_yaml)
        
    def execute(self):
        for execute in self.file:
            self.Client=socket.socket()
            host,port=self.file[execute]['Remote'],9000
            self.Client.connect((host,port))
            self.Client.sendall(str(execute).encode(encoding='utf_8'))
            self.Client.close()
    
    def results(self):
        
        self.Server=socket.socket()
        self.Endereco=(socket.gethostbyname(socket.gethostname()),9001)
        self.Server.bind(self.Endereco)
        #abrindo o numero de usuarios simultaneos igual ao tamanho de testes que iram rodar
        self.Server.listen(10)
        for f in self.file:
            c,addr =self.Server.accept()          
            #adicionando o client na lista de registro       
            
            with open('docs/results{}.zip'.format(str(addr[0]).replace(".", "")),'wb') as file:
                while(True):
                    teste=c.recv(1024)
                    if not teste:
                        break
                    file.write(teste)
                file.close()
            c.close()
        
class Runner_Client():
    def __init__(self,file_yaml):
        #abrindo um objeto socket
        self.Server=socket.socket()
        #recebendo todos os os parametros
        #pegando o tamanho de todos os testes para rodar 
        self.Endereco=(socket.gethostbyname(socket.gethostname()),9000)
        self.Server.bind(self.Endereco)
        #abrindo o numero de usuarios simultaneos igual ao tamanho de testes que iram rodar
        self.Server.listen(1)
        self.yaml=file_yaml
    def execute(self):  
        #criando uma lista para receber informações de todos os servidores  
        c,addr =self.Server.accept() 
        self.addr=addr         
        #adicionando o client na lista de registro
        self.instancia=c.recv(1024).decode('utf-8')
        os.system("python -m Pyautomators execute -f {yaml} -i {instancia}".format(yaml=self.yaml,instancia=self.instancia))
        #orquestrador(self.yaml,self.instancia)
        c.close()
        
    def results(self):
        
        self.Client=socket.socket()
        host,port=self.addr[0],9001
        try:
            os.mkdir('results')
        except:
            pass
        copy_tree("docs/", "results/docs/",verbose=True)
        copy_tree("docs/reports", "results/docs/reports/",verbose=True)
        copy_tree('log/',"results/logs/",verbose=True)
        shutil.make_archive('results',"zip",base_dir="results")
        self.Client.connect((host,port))
        with open('results.zip','rb') as file:
            f=file.read(1024)
            while f:
                self.Client.send(f)
                f=file.read(1024)
            file.close()
        shutil.rmtree('results', ignore_errors=True)
        os.remove('results.zip')
        self.Client.close()