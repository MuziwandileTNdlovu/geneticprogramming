import math
import random

import numpy as np

from BuildTree.Node import Node
from Config.Config import Config


class GeneticOperators:
    def __init__(self):
        self.config = Config()
        self.random = random.Random(self.config.getSeed())
        self.depth = self.config.MAX_DEPTH
        self.population = []

    def crossover(self, parent1, parent2):
        parent1_subtree = parent1.get_random_subtree(parent1, parent1)
        parent2_subtree = parent2.get_random_subtree(parent2, parent2)
        if self.random.random() < 0.5:
            if len(parent1_subtree.children) > 1:
                parent1_subtree.children[self.random.randint(0, 1)] = Node(parent2_subtree.name,
                                                                           children=[child for child in
                                                                                     parent2_subtree.children])
            else:
                parent1_subtree.children.append(
                    Node(parent2_subtree.name, children=[child for child in parent2_subtree.children]))

            return parent1_subtree
        else:
            if len(parent2_subtree.children) > 1:
                parent2_subtree.children[self.random.randint(0, 1)] = Node(parent1_subtree.name,
                                                                           children=[child for child in
                                                                                     parent1_subtree.children])
            else:
                parent2_subtree.children.append(
                    Node(parent1_subtree.name, children=[child for child in parent1_subtree.children]))

            return parent2_subtree

    def generateFull(self):
        if self.depth == 0:
            return Node(random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            self.depth -= 1
            left_child = self.generateFullWithDepth(self.depth)
            right_child = self.generateFullWithDepth(self.depth)
            return Node(random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    def generateFullWithDepth(self, depth):
        if depth == 0:
            return Node(random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            depth -= 1
            left_child = self.generateFullWithDepth(depth)
            right_child = self.generateFullWithDepth(depth)
            return Node(random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    @staticmethod
    def selection(population):
        population.sort(key=lambda x: list(x.keys())[0])
        n = len(population)
        percentile_index = math.ceil(0.1 * n) - 1
        fittest_individuals = population[:percentile_index]
        return fittest_individuals
