from DynamicCodeLoader import cargaCodigoDinamico
from LoaderKwirk import Loader
from UI import gui
from Kwirk import Level, State




"""
Clase Mediador

Implementa el patrón de diseño singleton

Interrelaciona las clases de interfaz entre si y con el modelo 
para que estas clases no tengan acoplamiento entre si.

"""

class Mediator(object):
    INSTANCE = None
    
    
    def __init__(self,modelPath, aStarPath, nodesPath):
        """ Constructor por defecto

        Devuelve un objeto de tipo mediador

        Parámetros:
        Ninguno.
        """ 
        self.solucion = []
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        # inicialización
        
        self.model = None
        self.search = None
        self.nodes = None
        self.manual = True
        
        if not modelPath is None:
            self.model = cargaCodigoDinamico(modelPath,"Model")
        
        if not aStarPath is None:
            self.search = cargaCodigoDinamico(aStarPath,"Search")
            self.manual = False

        if not nodesPath is None:
            self.nodes = cargaCodigoDinamico(nodesPath,"Nodes")
            self.manual = False
            
        

        

    @classmethod
    def get_instance(cls,modelPath = None, aStarPath = None, nodesPath = None):
        if cls.INSTANCE is None:
             cls.INSTANCE = Mediator(modelPath, aStarPath, nodesPath)
        return cls.INSTANCE
    
    
    
    def register_ui(self,ui):
        self.ui = ui
                
        desplegable, self.visor, control = ui.get_ui_elements().children
        
        
        direcciones, acciones = control.children
        
        
        box1, box2 = direcciones.children        
        empty,up,cambia=box1.children
        left,down,right=box2.children
        
        botones_accion = acciones.children
        
        l = Loader()
        levels = l.get_all_levels()
        
        desplegable.options = levels
        
        desplegable.observe(lambda name:self.update_level_observer(name), names='value') 
        
        self.filename = levels[0]
        self.update_level_from_file(self.filename)
        
        
        
        up.on_click(lambda button: self.button_action_event(button))
        down.on_click(lambda button: self.button_action_event(button))
        right.on_click(lambda button: self.button_action_event(button))
        left.on_click(lambda button: self.button_action_event(button))
        cambia.on_click(lambda button: self.button_action_event(button))

        
        for abutton in botones_accion:
            abutton.on_click(lambda button: self.button_action_event(button))
            
        
    def update_level_observer(self,name):
        self.filename=name['new']
        self.update_level_from_file(self.filename)
        
        
    def update_level_from_file(self,filename):
        
        level_txt = open("./levels/"+filename,'r').read()
        l = Loader()
        self.level, self.state = l.load_level(level_txt)
        htmlStr = self.ui.get_html(self.level, self.state)
        
        self.visor.value = htmlStr
        
        
    def actualiza_juego(self,desc):
        
               
        actualiza_turno = False
        mov = []
        if desc=="^":
            mov=[-1,0]
        elif desc=="v":
            mov=[1,0]
        elif desc==">":
            mov=[0,1]
        elif desc=="<":
            mov=[0,-1]
        elif desc=="Change":
            actualiza_turno = True
        
        if not mov == []:
            self.state=self.model.move(self.level,self.state,mov)
        elif actualiza_turno:            
            self.state = self.model.change_turn(self.state)
        else:
            #reinicio
            self.update_level_from_file(self.filename)
            self.solucion = []
            self.id_sol = 0
        
        
    def button_action_event(self,button):
        desc=button.description
        if desc in ["^","v","<",">","Change","Reiniciar"]:
            # Actualiza Juego
            self.actualiza_juego(desc)
        elif desc == "Resolver" and not self.search is None and not self.nodes is None:
                
                nodoInicial = self.nodes.nodo_inicial_Kwirk(self.level,self.state,self.nodes.heuristica_Kwirk)    
                
                self.solucion = self.search.AStar(nodoInicial,self.nodes.sucesores_Kwirk, self.nodes.meta_Kwirk, self.nodes.heuristica_Kwirk)
                self.num_evaluados = self.nodes.num_evaluados
                self.coste_total= self.nodes.coste_total
                self.id_sol = 0
            
        elif desc == "Siguiente":
                 
            if len(self.solucion) > 0 and len(self.solucion) > self.id_sol+1: 
                self.id_sol += 1
                s = self.solucion[self.id_sol]
                self.state = s
        elif desc == "Anterior":
            
            if len(self.solucion) > 0 and self.id_sol > 0: 
                self.id_sol -= 1
                s = self.solucion[self.id_sol]
                self.state = s
        
        
        htmlStr = self.ui.get_html(self.level, self.state)
        
        if not self.manual and len(self.solucion) > 0:
	        htmlStr+="<br/> Nodos evaluados <br/>" 
        	htmlStr+=str(self.num_evaluados)
        	htmlStr+="<br/> Coste de la solucion <br/>"
        	htmlStr+=str(self.coste_total)
        	htmlStr+="<br/> ______________ <br/>"

        self.visor.value = htmlStr
        

        
        if self.model.is_goal(self.state):
                    
            self.visor.value += "GANASTE!!!!! <br> Carga otro nivel"
