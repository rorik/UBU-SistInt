from ipywidgets import HTML, Dropdown ,Button, HBox, VBox, Box

"""
Clase que define los componentes gráficos de la interfaz

"""
class gui:
    
    
    def __init__(self, manual=True):
        """ Constructor por defecto

        Devuelve un objeto que crea la interfaz de usuario

        Parámetros:
        manual -- True (defecto) crea la interfaz para modo manual, false crea para modo automático
        """ 
        self.manual = manual
        self.element_image = {"grass": "./sprites/grass.png",
                              "wall": "./sprites/stones.png",
                              "destination": "./sprites/meta.jpg",
                              "player1": "./sprites/gazpacho.jpg",
                              "player2": "./sprites/pincho.jpg",
                              "box": "./sprites/caja.jpg",
                              "water": "./sprites/water.jpg"}
        
        
        # visor HTML donde se representará el juego
        visor=HTML()

        # Crea un desplegable con los niveles
        desplegable = Dropdown(description = 'Elija nivel:')

        # Botones para las direcciones
        up = Button(description="^")
        down = Button(description="v")
        right = Button(description=">")
        left = Button(description="<")
        cambia = Button(description="Change")

        empty=Button(description=" ")
        empty.margin=2
        
        

        direcciones=VBox([HBox([empty,up,cambia]),HBox([left,down,right])])
        acciones = self.get_actions()
        
        control = VBox([direcciones,acciones])
        
        self.ui=VBox(children=[desplegable, visor, control])
        
        
        
    def get_content(self,level,state,coord):
        """
        Obtiene el contenido de una determinada posición

        Parameters
        ----------
        coord : Posición [y,x] de la que queremos conocer el contenido

        Returns
        --------
        contenido : Una lista de tamaño 2 con el elemento del nivel y del estado en la coordenada
        """
        content = [None,None]
        
        
        
        board = level.get_board()
        destination =level.get_destination()
        
        boxes = state.get_boxes()
        water = state.get_water()
        players = state.get_players()

        if coord == destination:
            content[0] = "destination"
        elif board[coord[0]][coord[1]] == 0:
            content[0] = "grass"
        else:
            content[0] = "wall"

        if coord in boxes:
            content[1] = "box"

        if coord in water:
            content[1] = "water"


        if list(coord) == players[0]:
            content[1] = "player1"

        if list(coord) == players[1]:
            content[1] = "player2"


        return content
        
        

    def get_ui_elements(self):
        """ Obtiene los componentes gráficos del juego

        Devuelve un contenedor con los botones y el visor del juego
        
        Parámetros: 
        Ninguno
        """       
        

        return self.ui
    
    def get_actions(self):
        """         
        devuelve los botones de acción 
         en modo manual solo: reiniciar
         en modo automático: reiniciar, resolver, sig, anterior
        
        Parámetros: 
        Ninguno
        """       
        
        botones_accion = []
       
        reiniciar = Button(description="Reiniciar")
        botones_accion.append(reiniciar)
        
        if not self.manual:    
            
            resolver = Button(description="Resolver")
            siguiente = Button(description="Siguiente")
            anterior = Button(description="Anterior")
            botones_accion.append(resolver)
            botones_accion.append(siguiente)
            botones_accion.append(anterior)
            
            
        accciones = HBox(botones_accion)
        
        return accciones


    def get_html(self,level,state):
        """ 
        Obtiene la representación gráfica del juego en formato HTML

        Parámetros: 
        level- un nivel
        state - un estado
        """

        board = level.get_board()
        height = len(board)
        width = len(board[0])

        



        html_string = "<style> img.game {width: 50px !important; height: 50px !important;}</style><table>"



        new_row = "<tr>"
        end_row = "</tr>"

        for i in range(height):
            html_string+=new_row
            for j in range(width):

                content = self.get_content(level,state,(i,j))
                if content[1] is None:
                    drawing = self.element_image[content[0]]
                else:
                    drawing = self.element_image[content[1]]
                html = '<td><img class="game" src=%s alt=""></img></td>' % drawing     


                html_string+=html
            html_string+=end_row

        html_string += "</table>"


        return html_string



