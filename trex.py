import copy
import random
from time import sleep

import numpy as np
import pyautogui

from camera import Camera
from neural_network import NeuralNetwork


class TRex:
    def __init__(self):
        self.__genomes = [NeuralNetwork() for i in range(12)]
        self.__best_genomes = []

    def execute(self):
        camera = Camera()
        camera.find_environment()
        for genome in self.__genomes:
            camera.reset()
            pyautogui.click(200, 400)
            pyautogui.press('F5')
            sleep(1)
            pyautogui.press('space')

            while True:
                try:
                    obs = camera.find_next_obstacle()
                    inputs = [obs['distance'] / 1000, obs['length'], obs['speed'] / 10]
                    outputs = genome.forward_propagate(np.array(inputs, dtype=float))
                    print outputs[0]
                    if outputs[0] > 0.55:
                        print "JUMP"
                        pyautogui.press('space')
                except Exception as E:
                    print str(E)
                    break
            genome.fitness = camera.get_fitness()

    def keep_best_genomes(self):
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.__best_genomes = self.__genomes[:]

    def mutations(self):
        while len(self.__genomes) < 10:
            genome1 = random.choice(self.__best_genomes)
            genome2 = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(self.cross_over(genome1, genome2)))
        while len(self.__genomes) < 12:
            genome = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(genome))

    def cross_over(self, genome1, genome2):
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)
        cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]
        cut_location = int(len(new_genome.W2) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]
        return new_genome

    def __mutate_weights(self, weights):
        if random.uniform(0, 1) < 0.2:
            return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)
        new_genome.W1 += self.__mutate_weights(new_genome.W1)
        new_genome.W2 += self.__mutate_weights(new_genome.W2)
        return new_genome
