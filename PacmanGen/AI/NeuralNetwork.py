from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation


class NeuralNetwork(object):
    @staticmethod
    def get_new_model(board, output_nodes=4):
        board_size = board.size()
        model = Sequential()
        model.add(Dense(board_size * 2, activation='relu', input_shape=(board_size,), name='Game_Input'))
        model.add(Dense(int(board_size / output_nodes), activation='relu', name='Hidden_1'))
        model.add(Dense(output_nodes ** 2, activation='relu', name='Hidden_2'))
        model.add(Dense(output_nodes, activation='softmax', name='Game_Output'))
        return model
