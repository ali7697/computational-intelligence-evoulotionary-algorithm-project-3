import random
import statistics

import numpy as np

num_initial_generation = 100# This indicates the number of the weeks considered
num_iterations = 500
recombination_prob = 1
mutation_prob = 1
weeks = []
done = False
# First produce the initial population
for i in range(num_initial_generation):
    the_week = []
    day = []
    for d in range(7):
        day.append(random.sample(range(0, 9), 3))
        day.append(random.sample(range(-1, 0), 1))
        day.append(random.sample(range(0, 9), 4))
        day.append(random.sample(range(-1, 0), 1))
        day.append(random.sample(range(0, 9), 2))
        day = day[0] + day[1] + day[2] + day[3] + day[4]
        the_week.append(day)
        day = []
    weeks.append(the_week)

# related to mutation
# here I specify which indexes can be mutated
tmp1 = [0, 1, 2]
tmp2 = [4, 5, 6, 7]
tmp3 = [9, 10]
mutation_space = tmp1 + tmp2 + tmp3

# each time one of the rules are not being obeyed
# we reduce some points from the fitness
def cal_fitness(week):
    fitness = 1
    for da in week:
        shift1 = da[0:3]
        shift2 = da[4:8]
        shift3 = da[9:11]
        # first negative quality
        for dy in shift1:
            if dy in shift2 and dy != 0:
                fitness = fitness + 1
        for dy in shift2:
            if dy in shift3 and dy != 0:
                fitness = fitness + 1

        # second one
        for j in range(1, 9):
            if shift1.count(j) > 1:
                fitness = fitness + (shift1.count(j) - 1)
        for j in range(1, 9):
            if shift2.count(j) > 1:
                fitness = fitness + (shift2.count(j) - 1)
        for j in range(1, 9):
            if shift3.count(j) > 1:
                fitness = fitness + (shift3.count(j) - 1)

        # third
        if shift1.count(0) > 1:
            fitness = fitness + (shift1.count(0) - 1)
        if shift2.count(0) > 2:
            fitness = fitness + (shift2.count(0) - 2)
        if shift3.count(0) > 1:
            fitness = fitness + (shift3.count(0) - 1)

    # fourth
    for nurse in range(1, 9):
        repetitions = 0
        for dy in week:
            repetitions = repetitions + dy.count(nurse)
        if repetitions > 5:
            fitness = fitness + (repetitions - 5)
        if repetitions ==0 :
            fitness = fitness + 5
    fitness = 1 / fitness
    return fitness

# iterations
for it in range(num_iterations):
    children = []
    fitnesses = []
    # choosing the parents
    for pair in range(4 * num_initial_generation):
        parent1 = random.sample(weeks, 1)[0]
        parent2 = random.sample(weeks, 1)[0]
        child1 = []
        for i in parent1:
            child1.append(i[:])
        child2 = []
        for i in parent2:
            child2.append(i[:])

        # recombination should be done for each one of the days of the weeks
        if random.random() < recombination_prob:
            recombined_days = random.sample(range(7), 3)
            for day in recombined_days:
                single_point = random.randint(1, 10)  # the length of encoding is 11
                for i in range(single_point):
                    child1[day][i] = parent2[day][i]
                    child2[day][i] = parent1[day][i]
        # mutation
        if random.random() < mutation_prob:
            for day in range(7):
                indexes = random.sample(mutation_space, 2)
                tmp = child1[day][indexes[0]]
                child1[day][indexes[0]] = child1[day][indexes[1]]
                child1[day][indexes[1]] = tmp
        children.append(child1)
        children.append(child2)
        fitnesses.append(cal_fitness(child1))
        fitnesses.append(cal_fitness(child2))

    # selecting the survivors
    arr = np.array(fitnesses)
    encodings_key_indexes = arr.argsort()[-num_initial_generation:][::-1]
    weeks = []
    fitness_printing = []
    for ind in encodings_key_indexes:
        weeks.append(children[ind])
        fitness_printing.append(fitnesses[ind])
        if(fitnesses[ind]==1):
            answer = children[ind]
            done = True
    print(it)
    print('average: ', statistics.mean(fitness_printing))
    print('max: ', max(fitness_printing))
    print('min: ', min(fitness_printing))
    if done:
        print("done")
        print(answer)
        break
