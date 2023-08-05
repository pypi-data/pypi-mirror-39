# -*- coding: utf-8 -*-
'''
Created on 28 de out de 2018

@author: koliveirab
'''
import argparse,shutil
from Pyautomators.pyautomator import Project
from Pyautomators.Runner_Pyautomators import orquestrador
from Pyautomators.Runner_in_Container import Runner_Container
from Pyautomators import Ambiente
from Pyautomators.Documentacao import criar_documento_cliente
import os
from Pyautomators.remote import Runner_Client,Runner_Master
if('__main__'==__name__):
    print(""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""",
    """
                                                                                      ####   __  
        ##### #     # ##### #   # ###### ##### #       # ##### ###### ##### #####   ##     $$ _  
        #   #  #   #  #   # #   #    #   #   # ##     ## #   #    #   #   # #   #   ##    | | | 
        #####   # #   ##### #   #    #   #   # # #   # # #   #    #   #   # ####  \  ###   -_/   
        #        #    #   # #   #    #   #   # #  # #  # #####    #   #   # #  #   ##    ##      
        #       #     #   # #####    #   ##### #   #   # #   #    #   ##### #   #   #####        \n""",
    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""")
    ARG=argparse.ArgumentParser()
    ARG.add_argument("comando",help="""Comandos:
    criar_projeto:
    
    execute:
    
    exec_container
    
    
    """)
    ARG.add_argument('-f','--file_yaml',required=False,help='Arquivo Yaml base para execucoes em threads e containers')
    ARG.add_argument("-n",'--nome_projeto',required=False,help="Criar um projeto com a base do Pyautomators")
    ARG.add_argument("-d",'--diretorio',default=Ambiente.path_atual(),required=False,help="indique um diretorio para a execução das ações")
    ARG.add_argument('--volume_host',required=False,help="Volume do Host")
    ARG.add_argument('--volume_container',required=False,help="Volume do Container")
    ARG.add_argument('--master_host',required=False,help="ip do master")
    ARG.add_argument('--instancia',required=False,default=None,help='Instancia do Yaml a ser executada')
    ARG.add_argument("-i",'--retorn_result',default=False,help='retornar resultados')
    projeto=vars(ARG.parse_args())
    if(projeto['comando']=='criar_projeto'):
        Project.Criar_Projeto(projeto['nome_projeto'], projeto['diretorio'])
    elif(projeto['comando']=="execute"):
        Ambiente.irDiretorio(Ambiente._tratar_path(projeto['diretorio']))
        orquestrador(projeto["file_yaml"],projeto['instancia'])
    elif(projeto['comando']=="exec_container"):
        volume={projeto["volume_host"]:{"bind":projeto["volume_container"],"mode":"rw"}}
        Runner_Container().Runner_line(projeto["file_yaml"],volume)
    elif(projeto['comando']=="criar_doc"):
        Ambiente.irDiretorio(Ambiente._tratar_path(projeto['diretorio']))
        path=Ambiente.path_atual()
        v=1
        for jsons in os.listdir(path+'docs/reports/'):
            print(jsons)
            if(jsons.find('.json')!=-1):
                criar_documento_cliente(path+'docs/doc{}.doc'.format(v), path+'docs/reports/'+jsons, path+'docs/')
                v+=1
    elif(projeto['comando']=="Master_Remote"):
        runner=Runner_Master(projeto["file_yaml"])
        runner.execute()
        runner.results()
    elif(projeto['comando']=="Client_Remote"):
        runner=Runner_Client(projeto["file_yaml"])
        runner.execute()
        runner.results()
    elif(projeto['comando']=="Gerar_zip"):
        shutil.make_archive("docs/docs", "zip",  base_dir="docs")
        shutil.make_archive('docs/logs',"zip",base_dir="log")
    