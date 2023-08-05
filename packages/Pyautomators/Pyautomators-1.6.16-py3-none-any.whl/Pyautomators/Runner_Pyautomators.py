# -*- coding: utf-8 -*-

'''
Created on 26 de set de 2018

@author: koliveirab
'''
import argparse
from Pyautomators.BDT.__main__ import main as home
import threading
import ast
from Pyautomators.Error import Bdd_erro
from Pyautomators import Dados
from Pyautomators.Error import Ambiente_erro
from Pyautomators.Dados import pegarConteudoYAML
from Pyautomators import Ambiente  
import os
import sys

class Modelador_generico():
    def __init__(self,dicionario_yaml):
        self.dicionario_yaml=dicionario_yaml
        self.lista_de_execucao=['--summary','--no-logcapture','--no-capture-stderr','--no-capture']
        for item in self.dicionario_yaml:
            if(item=='Name'):
                self.lista_de_execucao.append("-Dname="+self.dicionario_yaml[item])
            elif(item=='Tags'):
                for arg in self.dicionario_yaml[item]:
                    tag_string=str(",").join(self.dicionario_yaml[item])
                self.lista_de_execucao.append("--tags="+tag_string)
            elif(item=='Args'):
                for arg in self.dicionario_yaml[item]:
                    self.lista_de_execucao.append('-D'+str(arg)+'='+str(self.dicionario_yaml[item][arg]))
        
class Modelador_Funcional_Web(Modelador_generico):
    
    
    def Run_Web(self,navegador):
        
        for item in self.dicionario_yaml:
            if(item=='Saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                self.lista_de_execucao.append('--junit')
                self.lista_de_execucao.append('--junit-directory='+dir)                        
                self.lista_de_execucao.append('--format=json.pretty')
                self.lista_de_execucao.append('-o='+dir+str(navegador)+"-"+self.dicionario_yaml["Name"]+"-"+self.dicionario_yaml[item])
                self.lista_de_execucao.append('--format=sphinx.steps')
                self.lista_de_execucao.append('-o=log/'+str(navegador)+"-"+self.dicionario_yaml["Name"])
                self.lista_de_execucao.append('--format=steps.doc')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-steps.log")
                self.lista_de_execucao.append('--format=steps.usage')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-features.log")
            
        self.lista_de_execucao.append('-Dnavegador='+navegador)
        return self.lista_de_execucao
    
class Modelador_Funcional_Mobile(Modelador_generico):
    def Run_Mobile(self,Device):
        
        for item in self.dicionario_yaml:
            if(item=='Saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                self.lista_de_execucao.append('--junit')
                self.lista_de_execucao.append('--junit-directory='+dir)                        
                self.lista_de_execucao.append('--format=json.pretty')
                self.lista_de_execucao.append('-o='+dir+str(Device)+"-"+self.dicionario_yaml["Name"]+"-"+self.dicionario_yaml[item])
                self.lista_de_execucao.append('--format=sphinx.steps')
                self.lista_de_execucao.append('-o=log/'+str(Device)+"-"+self.dicionario_yaml["Name"])
                self.lista_de_execucao.append('--format=steps.doc')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-steps.log")
                self.lista_de_execucao.append('--format=steps.usage')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-features.log")
            
        self.lista_de_execucao.append('-Ddevice='+Device)
        return self.lista_de_execucao
    
class Modelador_Funcional_Desktop(Modelador_generico):
    def Run_Desktop(self):
        
        for item in self.dicionario_yaml:
            if(item=='Saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                self.lista_de_execucao.append('--junit')
                self.lista_de_execucao.append('--junit-directory='+dir)                        
                self.lista_de_execucao.append('--format=json.pretty')
                self.lista_de_execucao.append('-o='+dir+self.dicionario_yaml["Name"]+"-"+self.dicionario_yaml[item])
                self.lista_de_execucao.append('--format=sphinx.steps')
                self.lista_de_execucao.append('-o=log/'+self.dicionario_yaml["Name"])
                self.lista_de_execucao.append('--format=steps.doc')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-steps.log")
                self.lista_de_execucao.append('--format=steps.usage')
                self.lista_de_execucao.append('-o='+"log/"+self.dicionario_yaml["Name"]+"-"+"location-features.log")
            
        return self.lista_de_execucao
    
class Thread_Run(threading.Thread):
    def __init__(self,list_exec,Item=None):
        threading.Thread.__init__(self)
        self.Item=Item
        self.list_exec=list_exec
    def run(self):  
        valor=None 
        if(self.list_exec['Tipo']=='Web'):
            valor=Modelador_Funcional_Web(self.list_exec).Run_Web(self.Item) 
        elif(self.list_exec['Tipo']=='Mobile'):
            valor=Modelador_Funcional_Mobile(self.list_exec).Run_Mobile(self.Item)
        elif(self.list_exec['Tipo']=='Desktop'):
            valor=Modelador_Funcional_Desktop(self.list_exec).Run_Desktop() 
        home(valor)

def runner(dicionario_de_execucao):
    lista_exec=[]
    if(dicionario_de_execucao['Tipo']=='Web'):
        for Navegador in dicionario_de_execucao['Navegadores']:
            lista_exec.append(Thread_Run(dicionario_de_execucao,Navegador))
    elif(dicionario_de_execucao['Tipo']=='Mobile'):
        for Device in dicionario_de_execucao['Devices']:
            lista_exec.append(Thread_Run(dicionario_de_execucao,Device))
    elif(dicionario_de_execucao['Tipo']=='Desktop'):
        lista_exec.append(Thread_Run(dicionario_de_execucao))
    for item in lista_exec:
        item.start()

def orquestrador(arquivo_yaml,espeficico=None):    
    testes=pegarConteudoYAML(arquivo_yaml)
    if( espeficico is None):
        for teste in testes: 
            if(str(teste).find("Teste")!=-1):
                runner(testes[teste])
            else:
                Error="""Configuração dos testes precisa ser parametrizada"""
                raise Bdd_erro(Error)
    else:
        runner(testes[espeficico])