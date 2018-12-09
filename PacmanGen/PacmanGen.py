import sys
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np

from Game.Gamestate import Gamestate
from Game.Board import get_default_board, get_default_food
from AI.NeuralNetwork import NeuralNetwork

if __name__ == '__main__':
    board = get_default_board()
    model = NeuralNetwork.get_new_model(board)
    for layer in model.layers:
        print(layer)
        #weights = layer.get_weights()

    # game = Gamestate(get_default_board(), get_default_food())
    # print(game)
    # while not game.has_ended():
    #     key = sys.stdin.read(1)
    #     if key == "w":
    #         game.move([-1, 0])
    #     elif key == "d":
    #         game.move([0, 1])
    #     elif key == "s":
    #         game.move([1, 0])
    #     elif key == "a":
    #         game.move([0, -1])
    #     print(game)
    #     print(game.score, game.moves)

