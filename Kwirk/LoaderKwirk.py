from os import listdir
from os.path import isfile, join

from Kwirk import Level, State

"""
Clase utilizada para cargar niveles a partir de su representación en ficheros de texto

"""
class Loader:
    
    def __init__(self):
    
        self.file_element = {"#": ['wall', None],
                             "@": ['grass', 'player1'],
                             "$": ['grass', 'player2'],
                             "+": ['grass', 'box'],
                             "*": ['destination', None],
                             "-": ['grass', 'water'],
                             " ": ['grass', None]}
    
    
    def get_all_levels(self):
        """ Obtiene la lista de niveles disponibles
        que son todos aquellos contenidos en la carpeta /levels/

        Devuelve una lista con los manejadores a ficheros contenidos en la carpeta de niveles 
        
        Parámetros: 
        Ninguno
        """
        
        mypath='./levels/'
        onlyfiles = [f for f in listdir(mypath) if f.startswith('level') and f.endswith('.txt') and isfile(join(mypath, f))]
        onlyfiles.sort()
        return onlyfiles
    
    
    def load_level(self,str_level):
        """ Carga un nivel a partir de un texto

        Devuelve un objeto de tipo State y otro de tipo Level
        
        Parámetros: 
        str_level - un string con la codificación del nivel
        """
        
        level = str_level.split("\n")
    
        board = []
        boxes = set()
        water = set()
        destination = () 

        player1,player2 = None, None
    
        i =0
        for row in level:
            board_row = []
            j =0
            for caracter in row:
                element = self.file_element[caracter]

                if element[0] == "wall":
                    board_row.append(1)
                else:
                    board_row.append(0)

                if element[1] =="player1":
                    player1 = [i,j]

                if element[1] =="player2":
                    player2 = [i,j]

                if element[1] =="box":
                    boxes.add((i,j))

                if element[1] =="water":
                    water.add((i,j))

                if element[0] == "destination":
                    destination = (i,j)

                j+=1
            i+=1
            if board_row:
                board.append(tuple(board_row))
    

        return Level(board,destination),State([player1,player2],boxes,water,True)
    
