'''
Created on 28 de out de 2018

@author: koliveirab
'''
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
class Js_Script():
    
    def __init__(self,drive):
        self.driver=drive
        
    def execute_script(self,script):
        '''Este metodo executa comando javascript no console do navegador
        
            parametros:
            script(obrigatorio):o script a ser executado
           Exemplo:
        ("window.scrollTo(0, document.body.scrollHeight);")'''
        #executa javascript no driver
        self.driver.execute_script(script)   
        
    def rolagem_tela(self,direcao):
        #executa a rolagem da tela pelo javascript
        '''Este metodo faz a rolagem da pagina que esta sendo usada em javaScript
        Exemplo: rolagem_tela('down')'''
        self.execute_script("mobile: scroll", {'direction': direcao})
        
    def rolagem_entre_elementos(self,de_elemento,para_elemento):
        #executa a rolagem da tela pelo javascript
        '''Este metodo faz a rolagem da pagina que esta sendo usada em javaScript
        Exemplo: rolagem_tela(elemento('1','id'),elemento('2','id'))'''
        self.execute_script("mobile: scrollBackTo", {de_elemento: para_elemento})
        
        
class Devices_info():
    
    def capacidades(self):
        #OK
        return self.driver.desired_capabilities
    
    def orientacao(self,orientacao='horizontal'):
        #OK
        if(orientacao=='horizontal'):
            self.driver.orientation = "LANDSCAPE"
        elif(orientacao=='vertical'):
            self.driver.orientation = "PORTRAIT"
    
    def set_localizacao_geografica(self,latitude:int,longitude:int,altitude:int):
        #OK
        return self.driver.set_location(latitude,longitude,altitude)
    
    def pacote_atual(self):   
        #OK
        return self.driver.current_package
        
    def zoom_elemento(self,elemmento,portentagem=200):
        self.driver.zoom_elemento(elemmento,portentagem)
    
    
    def atividade_atual(self):
        #OK
        return self.driver.current_activity

    
    def aguarde_em_segundo_plano(self,tempo:int):
        #OK
        self.driver.background_app(tempo*1000)
        
    def reiniciar(self):
        #OK
        self.driver.reset()
        
    def bloquear(self):
        #OK
        self.driver.lock()
        
    def desbloquear(self):
        #OK
        self.driver.unlock()
        
    def esconder_teclado(self):
        #OK
        self.driver.hide_keyboard()

    def abrir_notificacoes(self):
        #OK
        self.driver.open_notifications()
        
        
class Aguarde():
        
    def aguarde_execucao_script(self,tempo):
        self.driver.set_script_timeout(tempo)
        
        

class Verifica():
    
    def verifica_device_bloqueado(self):
        #OK
        return self.driver.is_locked()
    
    def verifica_teclado_visivel(self):
        #OK
        return self.driver.is_keyboard_shown()

    def verifica_se_selecionado(self,elemento):
        #OK        
        return elemento.is_selected()
    
    def verifica_se_elemento_ativo(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        return element.is_enabled()
    
    def verifica_se_elemento_visivel(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        return element.is_disabled()

class Simula_Touch():
    def __init__(self,driver):
        self._touch=TouchAction(driver)
        
    def clica_elemento(self,elemento,quantidade=1):
        #OK
        self._touch.tap(elemento,count=quantidade)
        return self
        
    def clica_coordenada(self,xi,yi,quantidade=1):
        #OK
        self._touch.tap(x=xi, y=yi, count=quantidade)
        return self
    
    def arrastar_elementos(self,elemento1,elemento2):
        
        self._touch.long_press(elemento1).move_to(elemento2).release()
        return self
    
    def arrastar_coordenada(self,xi,yi,xf,yf):
        
        self._touch.long_press(x=xi,y=yi).move_to(x=xf, y=yf).release()
        return self
    
    def soltar(self):
        #OK
        self._touch.release()
        return self
    
    def mover_elemento(self,elemento):
        
        self._touch.move_to(elemento)
        return self
    
    def mover_coordenada(self,xi,yi):
        self._touch.move_to(x=xi,y=yi)
        return self
    
    def pressionar_elemento_durante(self,elemento,duracao=5):
        #OK
        self._touch.long_press(elemento,duration=duracao*1000)
        return self 
    
    def pressionar_coordenada_durante(self,xi,yi,duracao=5):
        self._touch.long_press(x=xi,y=yi,duration=duracao*1000)
        return self
    
    def pausar(self,tempo):
        self._touch.wait(tempo*1000)
        return self
    
    def pegar_acoes(self):
        return self._touch
    
    def construir(self):
        self._touch.perform()
        
class Simula_MultiTouch():
    def __init__(self,driver,canais=2):
        self._multiAction=MultiAction(driver)
        self.canais=canais
        
    def adicionar_Acoes(self,*acoes):
        if len(acoes)>self.canais:
            raise Exception('Erro!')
        else:
            self._multiAction.add(*acoes)
        
        return self
    
    def construir(self):
        self._multiAction.perform()
        