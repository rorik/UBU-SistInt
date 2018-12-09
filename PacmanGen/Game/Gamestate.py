from Game.Board import Board, BoardState
import numpy as np


class Gamestate(object):
    score = 0
    moves = 0
    player = [23, 13]

    def __init__(self, board=None, food=None, moves_threshold=5000):
        # Board
        if board is None:
            board = Board()
        elif isinstance(board, Board):
            board = Board(board)
        self.board = board

        # Food
        self.food = food

        # Moves threshold
        self.moves_threshold = moves_threshold

        # Initialize position
        self.move([0, 0])

    def move(self, direction):
        self.moves += 1
        position = [self.player[0] + direction[0], self.player[1] + direction[1]]
        if self.board.get_element(position[0], position[1]) is Board.Feature.WALL:
            return False
        elif self.food.get_element(position[0], position[1]) is BoardState.Feature.FOOD:
            self.score += 10
            self.food.set_element(position[0], position[1], BoardState.Feature.EMPTY)
        self.player = position
        return True


    def has_ended(self):
        for row in self.food:
            if BoardState.Feature.FOOD in row:
                # Movements exceeded
                return self.moves >= self.moves_threshold
        # All food has been eaten
        return True

    def __str__(self):
        output = ""
        for i in range(len(self.board)):
            for j in range(len(self.board.get_row(i))):
                if self.player[0] == i and self.player[1] == j:
                    output += "@"
                elif self.board.get_element(i, j) is Board.Feature.WALL:
                    output += Board.Feature.WALL.value[0]
                elif self.food.get_element(i, j) is BoardState.Feature.FOOD:
                    output += BoardState.Feature.FOOD.value[0]
                else:
                    output += " "
            output += "\n"
        return output
