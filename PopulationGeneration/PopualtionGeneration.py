
import random

from Config.Config import Config
from BuildTree.Node import Node


class PopulationGeneration:

    def __init__(self, population_size):
        self.population_size = population_size
        self.config = Config()
        self.depth = self.config.getMaxDepth()
        self.population = []
        self.fitness = []
        self.fitness_sum = 0
        self.best_fitness = 0
        self.random = random.Random(self.config.getSeed())
        self.root_node = Node(self.random.choice(list(self.config.FUNCTION_SET.keys())))

    # generate right side
    def generateFull(self):
        if self.depth == 0:
            return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            self.depth -= 1
            left_child = self.generateFullWithDepth(self.depth)
            right_child = self.generateFullWithDepth(self.depth)
            return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    # generate left side
    def generateFullWithDepth(self, depth):
        if depth == 0:
            return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            depth -= 1
            left_child = self.generateFullWithDepth(depth)
            right_child = self.generateFullWithDepth(depth)
            return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    # generate right side
    def generateGrow(self):
        if self.depth <= self.config.MIN_DEPTH:
            if self.random.random() < 0.1:
                return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            self.depth -= 1
            if self.depth <= self.config.MIN_DEPTH:
                if self.random.random() < 0.5:
                    return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))

            else:
                self.depth -= 1
                left_depth = self.random.randint(self.config.MIN_DEPTH, self.depth)
                right_depth = self.depth - left_depth
                left_child = self.generateFullWithDepth(left_depth)
                right_child = self.generateFullWithDepth(right_depth)
                return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                            children=[left_child, right_child])

    # generate left side
    def generateFullWithDepthGrow(self, depth):
        if depth <= self.config.MIN_DEPTH  :
            if self.random.random() < 0.1:
                return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            depth -= 1
            if depth <= self.config.MIN_DEPTH:
                if self.random.random() < 0.5:
                    return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
            else:
                depth -= 1
                left_depth = self.random.randint(self.config.MIN_DEPTH, depth)
                right_depth = depth - left_depth
                left_child = self.generateFullWithDepth(left_depth)
                right_child = self.generateFullWithDepth(right_depth)
                return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                            children=[left_child, right_child])

    def full(self):
        for i in range(self.population_size):
            self.population.append(self.generateFull())
            self.depth = self.config.getMaxDepth()

    def grow(self):
        for i in range(self.population_size):
            self.population.append(self.generateGrow())
            self.depth = self.config.getMaxDepth()

    def rampedHalfAndHalf(self):
        for i in range(self.population_size):
            if i % 2 == 0:
                tree = self.generateFull()
                self.population.append(tree)
            else:
                tree = self.generateGrow()
                self.population.append(tree)
            self.depth = self.config.getMaxDepth()



    def getPopulation(self):
        return self.population
