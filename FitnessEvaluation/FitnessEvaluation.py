from Config.Config import Config
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error , r2_score , median_absolute_error

class FitnessEvaluation:
    def __init__(self, data):
        self.fitness_individual = []
        self.fitness_population = []
        self.config = Config()
        self.dataSet = data
        self.results_cache = {}

    def evaluatePopulation(self, population):
        for individual in population:
            for i in range(len(self.dataSet)):
                self.fitness_individual.append(self.evaluate(individual, self.dataSet.iloc[i]))
            self.fitness_population.append(
                {mean_absolute_error(self.dataSet["Duration"], self.fitness_individual  ): individual})
            self.fitness_individual = []
        return self.fitness_population

    def evaluateIndividual(self, individual):
        for i in range(len(self.dataSet)):
            self.fitness_individual.append(self.evaluate(individual, self.dataSet.iloc[i]))
        self.fitness_population.append({mean_absolute_error(self.dataSet["Duration"],self.fitness_individual ): individual})
        self.fitness_individual = []
        return self.fitness_population

    def evaluate(self, individual, dataset):
        if individual in self.results_cache:
            return self.results_cache[individual]

        if individual.name in self.config.TERMINAL_SET:
            result = dataset[individual.name]
        else:
            child_results = [self.evaluate(child, dataset) for child in individual.children]
            function = self.config.FUNCTION_SET[individual.name]
            if isinstance(child_results[0], np.ndarray):
                result = function(*child_results, out=np.empty_like(child_results[0]))
            else:
                result = function(*child_results)

        self.results_cache[individual] = result
        return result

    def removeWorstIndividuals(self, totalIndividualsToBeRemoved):
        for i in range(totalIndividualsToBeRemoved):
            self.fitness_population.sort(key=lambda x: list(x.keys())[0])
            self.fitness_population.pop(len(self.fitness_population) - 1)
        return self.fitness_population

    def getFitnessPopulation(self):
        return self.fitness_population

    def averageMae(self):
        return np.mean([list(obj.keys())[0] for obj in self.fitness_population])

    def setFitnessPopulation(self, fitness_population):
        self.fitness_population = fitness_population

    def getPopulation(self):
        return [list(obj.values())[0] for obj in self.fitness_population]

    def setDataSet(self, dataSet):
        self.dataSet = dataSet
