import numpy as np
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import deap

from Game.Gamestate import Gamestate
from Game.Board import get_default_board, get_default_food
from AI.NeuralNetwork import NeuralNetwork
from AI.Individual import Individual

moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def play(model, verbose=False):
    global moves
    moved = []
    game = Gamestate(get_default_board(), get_default_food(), max_moves)
    while not game.has_ended():
        input_data = game.get_data()
        predict = model.predict(input_data)[0]
        output = np.argmax(predict)
        move = moves[output]
        result = game.move(move)
        moved.append([output, result])
    if verbose:
        print(" ENDED WITH SCORE", game.score, "AFTER", game.moves, "MOVES")
    return game, moved


def evaluate(individual):
    result, moved = play(individual.model)
    fitness = 0
    #fitness = result.score / result.moves * 200
    for i in range(len(moved)):
        if False: #i - 2 >= 0:
            previous = (moved[i - 1][0] + 2) % 4
            previous2 = moved[i-2][0]
            if previous == previous2 == moved[i][0]:
                print(previous, previous2, moved[i][0])
                fitness += moved[i][1] * 3
                continue
        fitness += moved[i][1]
    return fitness


def breed(individual1, individual2):
    child = Individual(NeuralNetwork.get_new_model(board))
    for layer in range(len(individual1.model.layers)):
        shape = individual1.model.layers[layer].get_weights()[0].shape
        w1 = individual1.model.layers[layer].get_weights()[0].flatten()
        w2 = individual2.model.layers[layer].get_weights()[0].flatten()
        b1 = individual1.model.layers[layer].get_weights()[1]
        b2 = individual2.model.layers[layer].get_weights()[1]
        w_cut = int(random.random() * len(w1))
        b_cut = int(random.random() * len(b1))
        w = np.concatenate([w1[:w_cut], w2[w_cut:]])
        w = w.reshape(shape)
        b = np.concatenate([b1[:b_cut], b2[b_cut:]])
        child.model.layers[layer].set_weights(np.asarray([w, b]))
    return child


def mutate(individual):
    # print("Mutating", individual)
    # for layer in range(len(individual.model.layers)):
    #     w = individual.model.layers[layer].get_weights()[0]
    #     w_mask_min = np.invert(np.random.randint(0, int(1 / mutation_severity), size=w.shape).astype(np.bool))
    #     w_random_min = np.random.rand(*w.shape) * np.min(w)
    #     w_mask_max = np.invert(np.random.randint(0, int(1 / mutation_severity), size=w.shape).astype(np.bool))
    #     w_random_max = np.random.rand(*w.shape) * np.max(w)
    #     w[w_mask_min] = w_random_min[w_mask_min]
    #     w[w_mask_max] = w_random_max[w_mask_max]
    #     b = individual.model.layers[layer].get_weights()[1]
    #     b_mask_min = np.invert(np.random.randint(0, int(1 / mutation_severity), size=b.shape).astype(np.bool))
    #     b_random_min = np.random.rand(*b.shape) * (np.min(b))
    #     b_mask_max = np.invert(np.random.randint(0, int(1 / mutation_severity), size=b.shape).astype(np.bool))
    #     b_random_max = np.random.rand(*b.shape) * (np.max(b))
    #     b[b_mask_min] = b_random_min[b_mask_min]
    #     b[b_mask_max] = b_random_max[b_mask_max]
    #     individual.model.layers[layer].set_weights(np.asarray([w, b]))
    pass


def select(individuals):
    evaluation = []
    evaluation_stat = []
    for individual in individuals:
        result = evaluate(individual)
        evaluation.append([individual, result])
        evaluation_stat.append(result)

    # sort individuals by their evaluation
    evaluation.sort(key=lambda x: x[1], reverse=True)

    # keep the best individuals
    retained = int(population_size * retain)
    selected = [x[0] for x in evaluation[:retained]]

    for x in evaluation:
        result = play(x[0].model, True)
        print("--------")
        print(x[1])
        print(result[1])

    #result = play(selected[0].model, True)
    #print(selected[0].model.get_weights())
    #print(result[0])
    #print(result[1])
    #print(evaluation[0][1])

    # keep some of the "bad" individuals
    for non_parent in evaluation[retained:]:
        if random.random() <= retain_chance:
            selected.append(non_parent[0])
    return selected, evaluation_stat


def populate(individual_class, size=20):
    models = []
    for ignored in range(size):
        models.append(individual_class(NeuralNetwork.get_new_model(board, random=True)))
    return models


if __name__ == '__main__':

    board = get_default_board()

    generations = 1
    population_size = 8
    max_moves = 30
    retain = 0.3
    retain_chance = 0.1
    mutate_chance = 0.3
    mutation_severity = 0.1

    population = populate(Individual, population_size)

    for i in range(generations):
        parents, evaluation_stat = select(population)

        # Short-circuit if not enough parents
        if len(parents) < 2:
            raise RuntimeError("At least two parents are needed to advance to the next generation")

        new_population = []
        new_population.extend(parents)
        while len(new_population) < population_size:
            parent1 = random.randint(0, len(parents) - 1)
            parent2 = parent1
            while parent2 == parent1:
                parent2 = random.randint(0, len(parents) - 1)
            parent1 = parents[parent1]
            parent2 = parents[parent2]
            child = breed(parent1, parent2)
            if random.random() <= mutate_chance:
                mutate(child)
            new_population.append(child)

        population = new_population
        print("Generation %s (avg:%.2f, max:%.2f, min: %.2f)" % (i, sum(evaluation_stat) / len(evaluation_stat),
                                                                 max(evaluation_stat), min(evaluation_stat)))




    #nn_model = NeuralNetwork.get_new_model(board)
    #play(nn_model)