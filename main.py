import random
import time

import pandas as pd
from Config.Config import Config
from DataProcessing.Cleaning import DataCleaning
from FitnessEvaluation.FitnessEvaluation import FitnessEvaluation
from GeneticOperators.GeneticOperators import GeneticOperators
from PopulationGeneration.PopualtionGeneration import PopulationGeneration


def main():
    start_time = time.time()
    config = Config()
    randoms = random.Random(config.SEED)
    newDataSet = processData()
    operators = GeneticOperators()
    train, test = splitData(newDataSet)
    initPopulation = PopulationGeneration(config.POPULATION_SIZE)
    initPopulation.rampedHalfAndHalf()
    fitness = FitnessEvaluation(train)
    population = initPopulation.getPopulation()
    populationFitness = fitness.evaluatePopulation(population)
    selected = []

    for generation in range(config.MAX_GENERATIONS):
        selected = operators.selection(populationFitness)
        if randoms.random() < config.CROSSOVER_PROBABILITY:
            choice1 = randoms.choice(selected)
            choice2 = randoms.choice(selected)
            choice1 = list(choice1.values())[0]
            choice2 = list(choice2.values())[0]
            offspring = operators.crossover(choice1, choice2)
            populationFitness = fitness.evaluateIndividual(offspring)
        fitness.setFitnessPopulation(populationFitness)
        populationFitness = fitness.removeWorstIndividuals(len(populationFitness) - config.POPULATION_SIZE)

    RMSE = list(selected[0].keys())[0]
    print("AFTER TRAINING RMSE: ", RMSE)
    print("Average AFTER TRAINING MAE: ", fitness.averageMae())
    fitness.setDataSet(test)
    population = fitness.getPopulation()
    fitness.setFitnessPopulation([])
    populationFitness = fitness.evaluatePopulation(population)
    selected = operators.selection(populationFitness)
    RMSE = list(selected[0].keys())[0]
    print("FINAL RMSE: ", RMSE)
    print("Average FINAL MAE: ", fitness.averageMae())
    print("SEED: ", config.SEED)
    print("TIME TAKEN: ", time.time() - start_time, " seconds")


def processData():
    df = pd.read_csv('./dataset/preprocessed/For_modeling.csv')
    cleanData = DataCleaning(df)
    cleanData.selectFeatures()
    cleanData.addDuration()
    cleanData.removeOutliers()
    return cleanData.getdata()


def splitData(data):
    test_df = data.sample(n=Config().TESTING_DATA_SIZE, random_state=Config().SEED)
    train_df = data.drop(test_df.index).sample(n=Config().TRAINING_DATA_SIZE, random_state=Config().SEED)
    return train_df, test_df


if __name__ == "__main__":
    main()
