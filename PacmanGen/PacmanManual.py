import sys

from Game.Gamestate import Gamestate
from Game.Board import get_default_board, get_default_food
#import Game.Board

if __name__ == '__main__':
    game = Gamestate(get_default_board(), get_default_food())
    print(game)
    while not game.has_ended():
        key = sys.stdin.read(1)
        if key == "w":
            game.move([-1, 0])
        elif key == "d":
            game.move([0, 1])
        elif key == "s":
            game.move([1, 0])
        elif key == "a":
            game.move([0, -1])
        print(game)
        print(game.score, game.moves)