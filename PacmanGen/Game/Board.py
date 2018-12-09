import numpy as np
import pickle
from enum import Enum


class Map(object):
    def __init__(self, configuration=None):
        if configuration is None:
            self.matrix = None
        elif isinstance(configuration, Map):
            self.matrix = configuration.matrix.copy()
        elif isinstance(configuration, np.ndarray):
            self.matrix = configuration.copy()
        else:
            self.matrix = np.array(configuration)
    
    def add_rows(self, row):
        if self.matrix is None:
            self.matrix = np.array(row)
        else:
            self.matrix = np.vstack([self.matrix, row])

    def get_row(self, index):
        return self.matrix[index]

    def get_element(self, index_y, index_x):
        return self.get_row(index_y)[index_x]

    def set_element(self, index_y, index_x, value):
        self.get_row(index_y)[index_x] = value

    def add_row_from_string(self, row_string):
        row = np.empty([1,len(row_string)], self.Feature)
        for i, char in enumerate(row_string):
            feature = self.Feature.get_or_default(char)
            row[0][i] = feature
        self.add_rows(row)

    def __str__(self):
        result = ''
        for row in self:
            for element in row:
                result += element.value[0]
            result += '\n'
        return result

    def __len__(self):
        return len(self.matrix)

    def size(self):
        return self.matrix.size

    def shape(self):
        return self.matrix.shape

    def __iter__(self):
        return self.matrix.__iter__()

    def flatten(self):
        return self.matrix.flatten()

    class Feature(Enum):
        pass


class Board(Map):
    def __init__(self, configuration=None):
        Map.__init__(self, configuration)

    def is_path(self, index_y, index_x):
        return self.get_element(index_y, index_x) is Board.Feature.PATH

    class Feature(Enum):
        PATH = [' ', 0]
        WALL = ['#', 1]
        DOOR = ['+', 2]
        VOID = ['-', 3]

        @staticmethod
        def get_or_default(value):
            for feature in Board.Feature:
                if feature.value[0] is value:
                    return feature
            return Board.Feature.VOID

class BoardState(Map):
    def __init__(self, configuration=None):
        Map.__init__(self, configuration)

    def is_empty(self, index_y, index_x):
        return self.get_element(index_y, index_x) is BoardState.Feature.EMPT

    class Feature(Enum):
        EMPTY = [' ', 0]
        FOOD = ['.', 1]
        POWERUP = ['^', 2]
        FRUIT_ACTIVE = ['&', 3]
        FRUIT_INACTIVE = ['%', 0]

        @staticmethod
        def get_or_default(value):
            for feature in BoardState.Feature:
                if feature.value[0] is value:
                    return feature
            return BoardState.Feature.EMPTY


def get_default_board():
    board = Board()
    board.add_row_from_string("############################")
    board.add_row_from_string("#            ##            #")
    board.add_row_from_string("# #### ##### ## ##### #### #")
    board.add_row_from_string("# #--# #---# ## #---# #--# #")
    board.add_row_from_string("# #### ##### ## ##### #### #")
    board.add_row_from_string("#                          #")
    board.add_row_from_string("# #### ## ######## ## #### #")
    board.add_row_from_string("# #### ## ######## ## #### #")
    board.add_row_from_string("#      ##    ##    ##      #")
    board.add_row_from_string("###### ##### ## ##### ######")
    board.add_row_from_string("-----# ##### ## ##### #-----")
    board.add_row_from_string("-----# ##          ## #-----")
    board.add_row_from_string("-----# ## ###++### ## #-----")
    board.add_row_from_string("###### ## #      # ## ######")
    board.add_row_from_string("          #      #          ")
    board.add_row_from_string("###### ## #      # ## ######")
    board.add_row_from_string("-----# ## ######## ## #-----")
    board.add_row_from_string("-----# ##          ## #-----")
    board.add_row_from_string("-----# ## ######## ## #-----")
    board.add_row_from_string("###### ## ######## ## ######")
    board.add_row_from_string("#            ##            #")
    board.add_row_from_string("# #### ##### ## ##### #### #")
    board.add_row_from_string("# #### ##### ## ##### #### #")
    board.add_row_from_string("#   ##                ##   #")
    board.add_row_from_string("### ## ## ######## ## ## ###")
    board.add_row_from_string("### ## ## ######## ## ## ###")
    board.add_row_from_string("#      ##    ##    ##      #")
    board.add_row_from_string("# ########## ## ########## #")
    board.add_row_from_string("# ########## ## ########## #")
    board.add_row_from_string("#                          #")
    board.add_row_from_string("############################")
    return board

def get_default_food():
    food = BoardState()
    food.add_row_from_string("############################")
    food.add_row_from_string("#............##............#")
    food.add_row_from_string("#.####.#####.##.#####.####.#")
    food.add_row_from_string("#.#  #.#   #.##.#   #.#  #.#")
    food.add_row_from_string("#.####.#####.##.#####.####.#")
    food.add_row_from_string("#..........................#")
    food.add_row_from_string("#.####.##.########.##.####.#")
    food.add_row_from_string("#.####.##.########.##.####.#")
    food.add_row_from_string("#......##....##....##......#")
    food.add_row_from_string("######.##### ## #####.######")
    food.add_row_from_string("     #.##### ## #####.#     ")
    food.add_row_from_string("     #.##          ##.#     ")
    food.add_row_from_string("     #.## ######## ##.#     ")
    food.add_row_from_string("######.## #      # ##.######")
    food.add_row_from_string("      .   #      #   .      ")
    food.add_row_from_string("######.## #      # ##.######")
    food.add_row_from_string("     #.## ######## ##.#     ")
    food.add_row_from_string("     #.##          ##.#     ")
    food.add_row_from_string("     #.## ######## ##.#     ")
    food.add_row_from_string("######.## ######## ##.######")
    food.add_row_from_string("#............##............#")
    food.add_row_from_string("#.####.#####.##.#####.####.#")
    food.add_row_from_string("#.####.#####.##.#####.####.#")
    food.add_row_from_string("#...##................##...#")
    food.add_row_from_string("###.##.##.########.##.##.###")
    food.add_row_from_string("###.##.##.########.##.##.###")
    food.add_row_from_string("#......##....##....##......#")
    food.add_row_from_string("#.##########.##.##########.#")
    food.add_row_from_string("#.##########.##.##########.#")
    food.add_row_from_string("#..........................#")
    food.add_row_from_string("############################")
    return food

def export(array, file, convert=False):
    if convert:
        array = np.vectorize(lambda e: e.value[1])(array)
    pickle.dump(array, file=file)


if __name__ == '__main__':
    board = get_default_board()
    food = get_default_food()
    print(board, food)