'''
Created on 8 de nov de 2018

@author: koliveirab
'''
import logging
from Pyautomators.Error import Bdd_erro
import re
import sys
def setup(file_name='log/exec.log'):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',filename=file_name,filemode='w',level=logging.INFO)

def before_all(func,breaks=True):

    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Stage all, before:Sucess!")
        except Exception as e :
            logging.warning("...Stage all, before: Error!\nmsg.:"+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture
    
def before_feature(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Feature:{}, before:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Feature:{}, before:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture
    
def before_scenario(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Scenario:{}, before:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Scenario:{}, before:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture
    
def before_steps(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Step:{}, before:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Steps:{}, before:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture


    
def after_steps(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Step:{}, after:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Step:{}, after:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture

def after_scenario(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Scenario:{}, after:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Scenario:{}, after:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture

def after_feature(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Feature:{}, after:...Sucess!".format(args[1].name))
        except Exception as e :
            logging.warning("...Feature:{}, after:...Error:\nmsg.:".format(args[1].name)+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture

def after_all(func,breaks=True):
    def capture(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info("...Stage all, after:Sucess!")
        except Exception as e :
            logging.warning("...Stage all, after: Error!\nmsg.:"+str(e.args))
            if breaks ==True:
                Error="\n"+str(e.args)
                raise Bdd_erro(Error)
    return capture