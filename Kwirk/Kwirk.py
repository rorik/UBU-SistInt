"""
Define un estado del juego Kwirk

Las partes actualizables del juego como jugadores, agua y las cajas

Traduce comentarios al ingles
"""
class State:
    def __init__(self,players,boxes,water,turn):
        """ Constructor por defecto

        Devuelve un objeto de tipo State

        Parámetros:
        jugador -- coordenadas del jugador en forma de lista
        cajas -- set de tuplas de coordenadas de las cajas
        """  
        self.players = players
        self.boxes = boxes
        self.water = water
        self.turn = turn

        
    def get_players(self):
        """ Obtiene las coordenadas del jugador

        Devuelve lista con las coordenadas y,x del jugador

        Parámetros:
        Ninguno
        """   
        return self.players
    
    def get_boxes(self):
        """ Obtiene las coordenadas de las cajas

        Devuelve un set con y,x de cada una de las cajas, cada caja una tupla

        Parámetros:
        Ninguno
        """   
        return self.boxes
    
    
    def get_water(self):
        """ Obtiene las coordenadas de las cajas

        Devuelve un set con y,x de cada una de las cajas, cada caja una tupla

        Parámetros:
        Ninguno
        """   
        return self.water
    
    def get_turn(self):
        """ Obtiene las coordenadas de las cajas

        Devuelve un set con y,x de cada una de las cajas, cada caja una tupla

        Parámetros:
        Ninguno
        """   
        return self.turn
    
    
    
    def __str__(self):
        """ Obtiene la representación del objeto 

        Devuelve un string con la representación del objeto

        Parámetros:
        Ninguno
        """   
        return str(self.players)+str(self.boxes)+str(self.water)+str(self.turn)
    
    def __repr__(self):
        """ Obtiene la representación del objeto 

        Devuelve un string con la representación del objeto

        Parámetros:
        Ninguno
        """  
        return str(self.players)+str(self.boxes)+str(self.water)+str(self.turn)
    
    def __eq__(self,other):
        return all([self.players == other.players,
                    self.boxes == other.boxes,
                    self.water == other.water,
                    self.turn == other.turn])
    
    
    def __hash__(self):
        return hash((str(self.players), frozenset(self.boxes), frozenset(self.water), self.turn))
    
    
"""
Define un nivel del juego Kwirk

Las partes no-actualizables del juego como el el tablero y los destinos de cajas
"""    


class Level:
    
    def __init__(self,board,destination):
        """ Constructor por defecto

        Devuelve un objeto de tipo Level

        Parámetros:
        tablero -- lista de listas (lista 2D) que representa casillas libres y muros
        destinos -- frozenset de tuplas de coordenadas de los destinos
        """  
        self.board = board
        self.destination = destination
        
    def get_board(self):
        """ Devuelve el tablero

        Devuelve lista 2d, 0 en las posiciones libres, 1 en las posiciones donde hay un muro

        Parámetros:
        Ninguno
        """ 
        return self.board
    
    def get_destination(self):
        """ Obtiene las coordenadas de los destinos

        Devuelve un frozenset con y,x de cada una de los destinos, cada destino una tupla

        Parámetros:
        Ninguno
        """   
        return self.destination
    
    
    def __str__(self):
        """ Obtiene la representación del objeto 

        Devuelve un string con la representación del objeto

        Parámetros:
        Ninguno
        """   
        return str(self.board)+str(self.destination)
    
    def __repr__(self):
        """ Obtiene la representación del objeto 

        Devuelve un string con la representación del objeto

        Parámetros:
        Ninguno
        """   
        return str(self.board)+str(self.destination)
