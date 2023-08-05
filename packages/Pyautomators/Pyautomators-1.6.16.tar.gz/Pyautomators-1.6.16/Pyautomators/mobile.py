'''
@author: KaueBonfim
'''

from appium import webdriver as mob
from Pyautomators.Error import Elemento_erro
from Pyautomators.mobile_extesao import Js_Script,Simula_MultiTouch,Simula_Touch,Devices_info,Aguarde,Verifica

''' Este arquivo tem o intuito dos metodos em selenium para Desktop,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''
class Mobile(Js_Script,Devices_info,Aguarde,Verifica):
    def __init__(self,dicionario_caps,endereco='http://127.0.0.1:4723/wd/hub'):
        
        self.driver= mob.Remote(command_executor=endereco,desired_capabilities=dicionario_caps)     
        self.Touch=Simula_Touch
        self.MultiAction=Simula_MultiTouch
        
    def fechar_programa(self):
        self.driver.quit()
    
    def elemento(self,elemento,tipo,implicit=None):
        r'''Esta procura um elemento e retorna o objeto do elemento
        parametros:
        elemento(obrigatorio):elemento que deve ser procurado
        tipo(obrigatorio): tipo do elemento que sera procurado
        implicit: tempo que devemos esoerar o elemento aparecer, caso n�o apare�a e gerado um erro
        
        Exemplos:
        elemento("id.user","id",10)
        elemento("class_user_login","class",1)
        elemento("login","name")
           
        '''    
        if(implicit!=None):
            self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        elif(tipo == 'link'):            
            element=self.driver.find_element_by_link_text(elemento) 
        elif(tipo == 'tag'):            
            element=self.driver.find_element_by_tag_name(elemento) 
        elif(tipo == 'css'):            
            element=self.driver.find_element_by_css_selector(elemento) 
        elif(tipo == 'partial_link'):            
            element=self.driver.find_element_by_partial_link_text(elemento) 
        elif(tipo == 'accessibility_id'):
            element=self.driver.find_element_by_accessibility_id(elemento)
        elif(tipo == 'uiautomator'):
            element=self.driver.find_element_by_android_uiautomator(elemento)
        elif(tipo == 'image'):
            element=self.driver.find_element_by_image(elemento)
        elif(tipo == 'ios_class_chain'):
            element=self.driver.find_element_by_ios_class_chain(elemento)
        elif(tipo == 'ios_predicate'):
            element=self.driver.find_element_by_ios_predicate(elemento)
        elif(tipo == 'ios_uiautomation'):
            element=self.driver.find_element_by_ios_uiautomation(elemento)
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    
                name:    
                class:    
                xpath:    
                link:    
                tag:    
                css:    
                partial_link:   
                accessibility_id:
                uiautomator:
                image:
                ios_class_chain:
                ios_predicate:
                ios_uiautomation:
                """
            raise Elemento_erro(Erro)
        return element
        
    def clica(self,elemento,tipo,implicit=None):
        #OK
        '''Este metodo clica em um elemento, na qual temos tres parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
            
                clica("gsfi","class",10)
        '''
        element=self.elemento(elemento, tipo, implicit)
        element.click()
        return element
        
    
    def escreve(self,elemento,conteudo,tipo,implicit=None):
        #OK
        '''Este metodo escreve em um elemento, na qual temos cinco parametros
        
        elemento(obrigatorio): Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao.
        conteudo(obrigatorio): Conteudo na qual queremos inserir naquele elemento
        tipo(obrigatorio): O tipo para do elemento que iremos usar(id ,class, name, xpath ...)
        implicit: É o tempo que devemos esoerar o elemento aparecer, caso não apareça e gerado um erro
        
        Exemplos:
        
                 escreve("gsfi","QUALQUER TEXTO","class",10)
        '''
        element=self.elemento(elemento, tipo, implicit)
        element.send_keys(conteudo)
        return element
    
    def voltar(self):
        #OK
        self.driver.back()
        
    def pressionar_coordenada(self,xi,yi,xf,yf,duracao=None):
        #OK
        self.driver.tap([(xi,yi),(xf,yf)],duracao*1000)
       
    def print_device(self,path_imagem:str):
        #OK
        '''Este metodo tira um print do conteudo atual da janela sendo usada
        
            parametros:
            path_imagem(obrigatorio):nome a imagem mais o caminho dela caso seja em outro diretorio
           Exemplo:
        print_janela('c:/teste.png')
        print_janela('teste.png')'''
        
        self.driver.get_screenshot_as_file(path_imagem)
    
    def limpar(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        element.clear()
        return element
    
    def pegar_texto(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        return element.text
    
    def pegar_tag_name(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        return element.tag_name
    
    def pegar_coordenadas(self,elemento,tipo,implicit=None):
        #OK
        element=self.elemento(elemento, tipo, implicit)
        coordenadas=[]
        x,y=element.location['x'],element.location['y']
        coordenadas.append(x)
        coordenadas.append(y)
        h,w=element.size['height'],element.size['width']
        coordenadas.append(h)
        coordenadas.append(w)
        return tuple(coordenadas)
    

    def pegar_instancia_mobile(self):
        #OK
        return self.driver