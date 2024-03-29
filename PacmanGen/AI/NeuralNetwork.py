from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import RandomNormal


class NeuralNetwork(object):
    @staticmethod
    def get_new_model(board, output_nodes=4, random=False):
        board_size = board.size()
        model = Sequential()
        initializer = RandomNormal(mean=0.0, stddev=0.4, seed=None) if random else 'zeros'
        model.add(Dense(board_size*2, activation='relu', input_shape=(board_size,), name='Game_Input',
                        kernel_initializer=initializer, input_dtype=float))
        model.add(Dense(int(board_size / output_nodes), activation='relu', name='Hidden_1',
                        kernel_initializer=initializer, input_dtype=float))
        model.add(Dense(output_nodes ** 2, activation='relu', name='Hidden_2',
                        kernel_initializer=initializer, input_dtype=float))
        model.add(Dense(output_nodes, activation='relu', name='Game_Output',
                        kernel_initializer=initializer, input_dtype=float))
        return model
