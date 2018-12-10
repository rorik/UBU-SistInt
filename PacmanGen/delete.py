"""Entry point to evolving the neural network. Start here."""
import logging
from optimizer import Optimizer
from tqdm import tqdm

# Setup logging.
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='log.txt'
)

def train_networks(networks, dataset):
    """Train each network.

    Args:
        networks (list): Current population of networks
        dataset (str): Dataset to use for training/evaluating
    """
    pbar = tqdm(total=len(networks))
    for network in networks:
        network.train(dataset)
        pbar.update(1)
    pbar.close()

def get_average_accuracy(networks):
    """Get the average accuracy for a group of networks.

    Args:
        networks (list): List of networks

    Returns:
        float: The average accuracy of a population of networks.

    """
    total_accuracy = 0
    for network in networks:
        total_accuracy += network.accuracy

    return total_accuracy / len(networks)

def generate(generations, population, nn_param_choices, dataset):
    """Generate a network with the genetic algorithm.

    Args:
        generations (int): Number of times to evole the population
        population (int): Number of networks in each generation
        nn_param_choices (dict): Parameter choices for networks
        dataset (str): Dataset to use for training/evaluating

    """
    optimizer = Optimizer(nn_param_choices)
    networks = optimizer.create_population(population)

    # Evolve the generation.
    for i in range(generations):
        logging.info("***Doing generation %d of %d***" %
                     (i + 1, generations))

        # Train and get accuracy for networks.
        train_networks(networks, dataset)

        # Get the average accuracy for this generation.
        average_accuracy = get_average_accuracy(networks)

        # Print out the average accuracy each generation.
        logging.info("Generation average: %.2f%%" % (average_accuracy * 100))
        logging.info('-'*80)

        # Evolve, except on the last iteration.
        if i != generations - 1:
            # Do the evolution.
            networks = optimizer.evolve(networks)

    # Sort our final population.
    networks = sorted(networks, key=lambda x: x.accuracy, reverse=True)

    # Print out the top 5 networks.
    print_networks(networks[:5])

def print_networks(networks):
    """Print a list of networks.

    Args:
        networks (list): The population of networks

    """
    logging.info('-'*80)
    for network in networks:
        network.print_network()

def main():
    """Evolve a network."""
    generations = 10  # Number of times to evole the population.
    population = 20  # Number of networks in each generation.
    dataset = 'cifar10'

    nn_param_choices = {
        'nb_neurons': [64, 128, 256, 512, 768, 1024],
        'nb_layers': [1, 2, 3, 4],
        'activation': ['relu', 'elu', 'tanh', 'sigmoid'],
        'optimizer': ['rmsprop', 'adam', 'sgd', 'adagrad',
                      'adadelta', 'adamax', 'nadam'],
    }

    logging.info("***Evolving %d generations with population %d***" %
                 (generations, population))

    generate(generations, population, nn_param_choices, dataset)

if __name__ == '__main__':
    main()

    """
    Class that holds a genetic algorithm for evolving a network.

    Credit:
        A lot of those code was originally inspired by:
        http://lethain.com/genetic-algorithms-cool-name-damn-simple/
    """
    from functools import reduce
    from operator import add
    import random
    from network import Network


    class Optimizer():
        """Class that implements genetic algorithm for MLP optimization."""

        def __init__(self, nn_param_choices, retain=0.4,
                     random_select=0.1, mutate_chance=0.2):
            """Create an optimizer.

            Args:
                nn_param_choices (dict): Possible network paremters
                retain (float): Percentage of population to retain after
                    each generation
                random_select (float): Probability of a rejected network
                    remaining in the population
                mutate_chance (float): Probability a network will be
                    randomly mutated

            """
            self.mutate_chance = mutate_chance
            self.random_select = random_select
            self.retain = retain
            self.nn_param_choices = nn_param_choices

        def create_population(self, count):
            """Create a population of random networks.

            Args:
                count (int): Number of networks to generate, aka the
                    size of the population

            Returns:
                (list): Population of network objects

            """
            pop = []
            for _ in range(0, count):
                # Create a random network.
                network = Network(self.nn_param_choices)
                network.create_random()

                # Add the network to our population.
                pop.append(network)

            return pop

        @staticmethod
        def fitness(network):
            """Return the accuracy, which is our fitness function."""
            return network.accuracy

        def grade(self, pop):
            """Find average fitness for a population.

            Args:
                pop (list): The population of networks

            Returns:
                (float): The average accuracy of the population

            """
            summed = reduce(add, (self.fitness(network) for network in pop))
            return summed / float((len(pop)))

        def breed(self, mother, father):
            """Make two children as parts of their parents.

            Args:
                mother (dict): Network parameters
                father (dict): Network parameters

            Returns:
                (list): Two network objects

            """
            children = []
            for _ in range(2):

                child = {}

                # Loop through the parameters and pick params for the kid.
                for param in self.nn_param_choices:
                    child[param] = random.choice(
                        [mother.network[param], father.network[param]]
                    )

                # Now create a network object.
                network = Network(self.nn_param_choices)
                network.create_set(child)

                # Randomly mutate some of the children.
                if self.mutate_chance > random.random():
                    network = self.mutate(network)

                children.append(network)

            return children

        def mutate(self, network):
            """Randomly mutate one part of the network.

            Args:
                network (dict): The network parameters to mutate

            Returns:
                (Network): A randomly mutated network object

            """
            # Choose a random key.
            mutation = random.choice(list(self.nn_param_choices.keys()))

            # Mutate one of the params.
            network.network[mutation] = random.choice(self.nn_param_choices[mutation])

            return network

        def evolve(self, pop):
            """Evolve a population of networks.

            Args:
                pop (list): A list of network parameters

            Returns:
                (list): The evolved population of networks

            """
            # Get scores for each network.
            graded = [(self.fitness(network), network) for network in pop]

            # Sort on the scores.
            graded = [x[1] for x in sorted(graded, key=lambda x: x[0], reverse=True)]

            # Get the number we want to keep for the next gen.
            retain_length = int(len(graded) * self.retain)

            # The parents are every network we want to keep.
            parents = graded[:retain_length]

            # For those we aren't keeping, randomly keep some anyway.
            for individual in graded[retain_length:]:
                if self.random_select > random.random():
                    parents.append(individual)

            # Now find out how many spots we have left to fill.
            parents_length = len(parents)
            desired_length = len(pop) - parents_length
            children = []

            # Add children, which are bred from two remaining networks.
            while len(children) < desired_length:

                # Get a random mom and dad.
                male = random.randint(0, parents_length - 1)
                female = random.randint(0, parents_length - 1)

                # Assuming they aren't the same network...
                if male != female:
                    male = parents[male]
                    female = parents[female]

                    # Breed them.
                    babies = self.breed(male, female)

                    # Add the children one at a time.
                    for baby in babies:
                        # Don't grow larger than desired length.
                        if len(children) < desired_length:
                            children.append(baby)

            parents.extend(children)

            return parents