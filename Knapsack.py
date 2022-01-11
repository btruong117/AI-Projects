#Brian Truong
#CS 3642 2021
#Assignment 3

import random as r
import pdb

CAPACITY = 65
string_size = 30
pop_size = 500
num_generations = 2000
p_cross = 0.8
p_mut = 0.05
# derived from online calculator
TARGET_FITNESS = 457
values = [1, 23, 5, 18, 31, 14, 23, 35, 4, 34, 12, 15, 34,
          16, 25, 39, 15, 9, 40, 38, 40, 16, 24, 40, 38, 31, 38, 5, 33, 37]
weights = [3, 2, 1, 1, 6, 6, 3, 4, 4, 3, 2, 10, 10, 3, 4,
           8, 3, 9, 10, 7, 10, 10, 7, 5, 3, 5, 9, 8, 6, 6]


# calculates the fitness(total value of items represented in string)
def fitness(candidate):
    total_val = 0
    total_wt = 0
    for i in range(len(candidate)):
        if candidate[i] == 1:
            total_val += values[i]
            total_wt += weights[i]
    # strings whose weights are greater than capacity have a fitness of 0,
    # otherwise fitness of a string is the total value of the items that it represents
    if total_wt <= CAPACITY:
        return total_val
    else:
        return 0


# returns the string with the highest fitness score for a given population
def get_fittest(pop):
    fittest = pop[0]
    for i in range(len(pop)):
        if fitness(pop[i]) > fitness(fittest):
            fittest = pop[i]

    return fittest


# performs 2 point cross over
def crossover(p1, p2, cross_rate):
    c1, c2 = p1.copy(), p2.copy()
    if r.random() < cross_rate:
        # crossover points are at 1/3 and 2/3 the length of the given string respectively
        cross_point1 = int(len(c1) / 3)
        cross_point2 = int(2 * (len(c1) / 3))
        c1 = p1[:cross_point1] + p2[cross_point1:cross_point2] + p1[cross_point2:]
        c2 = p2[:cross_point1] + p1[cross_point1:cross_point2] + p2[cross_point2:]

    return c1, c2


# performs mutation
def mutation(candidate, mut_rate):
    for m in range(len(candidate)):
        if r.random() < mut_rate:
            candidate[m] = abs(1 - candidate[m])
    return candidate


# returns list of strings whose weights are within the capacity of the knapsack
def viable_candidates(pop):
    candidates = []
    for i in range(len(pop)):
        if fitness(pop[i]) > 0:
            candidates.append(pop[i])

    return candidates


# tournament selection on strings that have fitness greater than 0
def selection(samp):
    cand = viable_candidates(samp)
    parents = []
    # chooses fittest candidates by comparing two random candidates to each other, then appends to parent list
    for p in range(int(len(cand) * 0.7)):
        i1 = r.randint(0, len(cand) - 1)
        i2 = r.randint(0, len(cand) - 1)
        if fitness(cand[i1]) > fitness(cand[i2]):
            parents.append(cand[i1])
        else:
            parents.append(cand[i2])

    return parents


def genetic_algorithm(gens, cross_rate, mut_rate):
    # sets random initial population
    population = [[r.randint(0, 1) for y in range(string_size)] for x in range(pop_size)]
    best_string, best_value = [[0]], 0
    for g in range(gens):  # GA runs until the target fitness is reached or the number of generations has been met
        if best_value == TARGET_FITNESS:
            return "Final string generated: " + str([best_string, best_value])
        parents = selection(population)  # list of parents who will be subject to reproduction operators
        children = []  # offspring of parents
        for p in range(len(parents)):
            # perform crossover between two random parent strings in the selected population
            i1 = r.randint(0, len(parents) - 1)
            i2 = r.randint(0, len(parents) - 1)
            # sets the two resulting children from crossover to child
            child = crossover(parents[i1], parents[i2], cross_rate)
            # performs mutation on children from cross over and appends them to list of children
            for c in child:
                children.append(mutation(c, mut_rate))
        # if the amount of children generated is the not the size of the orignial population,
        # add random strings to children until population size is met
        cand_needed = pop_size - len(children)
        for h in range(cand_needed):
            children.append([r.randint(0, 1) for y in range(string_size)])
        # sets the next population as the children of the previous generation
        population = children
        # recalculates the fittest string and its fitness value
        if fitness(get_fittest(population)) > fitness(best_string):
            best_string = get_fittest(population)
            best_value = fitness(best_string)
        # shows the fittest string for the current generation
        print("Best string for: %dth generation" % g)
        print(best_string)
        print("Fitness of best string: %d\n" % best_value)
        # print(population)
    # returns fittest string after max number of generations were reached or the target fitness is met
    return "Final string generated: " + str([best_string, best_value])


print(genetic_algorithm(num_generations, p_cross, p_mut))
