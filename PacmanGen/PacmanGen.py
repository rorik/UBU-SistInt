import numpy as np
import random
import argparse
import pickle
import time

from Game.Gamestate import Gamestate
from Game.Board import BoardState, get_default_board, get_default_food
from AI.NeuralNetwork import NeuralNetwork
from AI.Individual import Individual

moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def play(model, verbose=False):
    global moves
    moved = []
    visited = []
    game = Gamestate(board, BoardState(food), max_moves)
    while not game.has_ended():
        input_data = game.get_data()
        predict = model.predict(input_data)[0]
        output = np.argmax(predict)
        move = moves[output]
        result = game.move(move)
        moved.append([output, result])
        if result == -5:  # Wall, neural network can't advance
            break
        if result > 0:  # Food, reset visited nodes
            visited = []
        else:
            if any(pos[0] == game.player[0] and pos[1] == game.player[1] for pos in visited):
                break  # Already was in this state, neural network can't advance
        visited.append(game.player)
    if verbose:
        print(" ENDED WITH SCORE", game.score, "AFTER", game.moves, "MOVES")
    return game, moved


def evaluate(individual):
    result, moved = play(individual.model)
    fitness = len([move for move in moved if move[1] > 0])
    return fitness, moved


def breed(individual1, individual2):
    child = Individual(NeuralNetwork.get_new_model(board))
    for layer in range(len(individual1.model.layers)):
        # Breed the weights
        w1 = individual1.model.layers[layer].get_weights()[0]
        w_mask = np.random.randint(0, int(random.random() * w1.size)+1, size=w1.shape).astype(np.bool)
        w = np.copy(w1)
        w[w_mask] = individual2.model.layers[layer].get_weights()[0][w_mask]
        # Breed the biases
        b1 = individual1.model.layers[layer].get_weights()[1]
        b_mask = np.random.randint(0, int(random.random() * b1.size)+1, size=b1.shape).astype(np.bool)
        b = np.copy(b1)
        b[b_mask] = individual2.model.layers[layer].get_weights()[1][b_mask]
        child.model.layers[layer].set_weights(np.asarray([w, b]))
    return child


def mutate(individual):
    for layer in range(len(individual.model.layers)):
        w = individual.model.layers[layer].get_weights()[0]
        w_mask = np.invert(np.random.randint(0, int(1 / mutation_severity), size=w.shape).astype(np.bool))
        w_random = np.random.uniform(low=-1, high=1, size=w.shape)
        w[w_mask] = w_random[w_mask]
        b = individual.model.layers[layer].get_weights()[1]
        b_mask = np.invert(np.random.randint(0, int(1 / mutation_severity), size=b.shape).astype(np.bool))
        b_random = np.random.uniform(low=-1, high=1, size=b.shape)
        b[b_mask] = b_random[b_mask]
        individual.model.layers[layer].set_weights(np.asarray([w, b]))


def select(individuals):
    evaluation = []
    evaluation_stat = []
    for individual in individuals:
        result = evaluate(individual)
        evaluation.append([individual, result])
        evaluation_stat.append(result[0])

    # sort individuals by their evaluation
    evaluation.sort(key=lambda x: x[1][0], reverse=True)

    # Store the best individual
    best.append([evaluation[0][1][0], evaluation[0][1][1], evaluation[0][0].model.to_json()])

    # Keep the best individuals
    retained = int(population_size * retain)
    selected = [x[0] for x in evaluation[:retained]]

    # Keep some of the "bad" individuals
    for non_parent in evaluation[retained:]:
        if random.random() <= retain_chance:
            selected.append(non_parent[0])

    # If not enough individuals, add a random one
    while len(selected) < 2:
        selected.append(random.choice(evaluation)[0])

    return selected, evaluation_stat


def populate(individual_class, size=20):
    models = []
    for ignored in range(size):
        models.append(individual_class(NeuralNetwork.get_new_model(board, random=True)))
    return models


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pacman genetic neural network algorithm.')
    parser.add_argument("-l", "--load", type=str, help="load the population from a file")
    parser.add_argument("-s", "--save", type=str, help="save the population to a file")
    parser.add_argument("-b", "--best", type=str, help="save the best individual of each generation to a file")
    parser.add_argument("-g", "--generations", type=int, help="save the best individual of each generation to a file")
    args = parser.parse_args()

    board = get_default_board()
    food = get_default_food()

    if args.generations:
        generations = args.generations
    else:
        generations = 20
    population_size = 10
    max_moves = 300
    retain = 0.3
    retain_chance = 0.1
    mutate_chance = 0.2
    mutation_severity = 0.1

    if args.load is not None:
        print("Loading population from file")
        population = []
        try:
            with open(args.load, "rb") as file:
                loaded = pickle.load(file)
                for weights in loaded:
                    model = NeuralNetwork.get_new_model(board)
                    model.set_weights(weights)
                    population.append(Individual(model))
        except IOError:
            print("Error reading file")
            raise
    else:
        population = populate(Individual, population_size)
    best = []
    for i in range(generations):
        start = time.time()

        # Get the new parents
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
        end = time.time()
        print("Generation %s (avg:%.2f, max:%.2f, min: %.2f) took %.2fs" %
              (i, sum(evaluation_stat) / len(evaluation_stat), max(evaluation_stat), min(evaluation_stat), end - start))
        if i == generations - 1 and args.save is not None:
            output = [individual.model.get_weights() for individual in population]
            with open(args.save, "wb") as file:
                pickle.dump(output, file)

    if args.best is not None:
        with open(args.best, "a+") as file:
            file.writelines(["%d %% %s %% %s\n" % (record[0], record[1], record[2]) for record in best])
