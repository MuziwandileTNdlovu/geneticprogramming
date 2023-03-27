import sys
import math
class Config:
    def __init__(self):
        self.TERMINAL_SET = {
            "Distance": "1",
            "Haversine": "2",
            "Phour": "3",
            "PDweek": "4",
            "Dhour": "5",
            "DDweek": "6",
            "Temp": "7",
            "Wind": "8",
            "Humid": "9",
            "GroundTemp": "10"}

        self.FUNCTION_SET = {
            '+': lambda x, y=None: x if y is None else x + y,
            '-': lambda x, y=None: x if y is None else x - y,
            '*': lambda x, y=None: x if y is None else x * y,
            '/': lambda x, y=None: x if y is None else 1 if y == 0 else x / y,
            "sqrt": lambda x, y=None: math.sqrt(abs(x)),

        }
        self.SEED = int(sys.argv[1])
        self.MIN_DEPTH = 3
        self.MAX_DEPTH = 6
        self.POPULATION_SIZE = 100
        self.MAX_GENERATIONS = 500
        self.CROSSOVER_PROBABILITY = 0.9
        self.MUTATION_PROBABILITY = 0.1
        self.TESTING_DATA_SIZE = 20000
        self.TRAINING_DATA_SIZE = 50000

    def getTerminal(self, index):
        return self.TERMINAL_SET[index]

    def getFunction(self, index):
        return self.FUNCTION_SET[index]

    def getSeed(self):
        return self.SEED

    def getMaxDepth(self):
        return self.MAX_DEPTH

    def setSeed(self, num):
        self.SEED = num
