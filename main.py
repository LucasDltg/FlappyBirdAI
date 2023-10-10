import random
import time
import sys
import numpy
import flappybird


population_size = 100
bound = 2
population = []
generation = 100
mutation = 0.09
crossing = 0.70


def init_population():
    l = []
    for i in range(0, population_size):
        t = []
        for j in range(0, 11):
            t.append(random.uniform(-bound, bound))
        l.append(t)
    return l


if len(sys.argv) > 1:
    last_line= []
    with open(sys.argv[1], "r") as f:
        for line in f:
            pass
        last_line = line

    last_line = last_line.replace('[', '')
    last_line = last_line.replace(']', '')
    w = [list(map(float, last_line.split(',')))]

    flappybird.startGame(w, graphic_enable=True, fps=60)
    sys.exit()


path = str("Generation_data/"+"a"+".txt")
file = open(path, "w")

population = init_population()

for i in range(0, generation):
    new_population = []
    print("Generation " + str(i))

    #evaluation des modeles
    scores = flappybird.startGame(population, graphic_enable=True, fps=10000)

    #trouve le meilleur
    max=0
    max_ind = 0
    for j in range(0, len(population)):
        if scores[j] > max:
            max = scores[j]
            max_ind = j
    #ajoute le meilleur
    new_population.append(population[max_ind])
    file.write("---- Generation "+str(i)+" ----\n")
    file.write(str(population.pop(max_ind)) + "\n")
    scores.pop(max_ind)

    #trouve les autres avec tournoi 2 avec rous biaisé
    for j in range(0, int(population_size/2-1)):
        #array de proba
        c = numpy.cumsum(numpy.array(scores)/numpy.sum(scores))
        a = random.randint(0, 10000)/10000

        for k in range(0, len(c)):
            if c[k] >= a:
                a = k
                break
        new_population.append(population[a])
        population.pop(a)
        scores.pop(a)

    #croisement
    for j in range(0, int(population_size/4)):
        e1 = new_population[j*2].copy()
        e2 = new_population[j*2+1].copy()
        for k in range(0, 11):
            if random.randint(0, 100) < crossing*100:
                t = e1[k]
                e1[k] = e2[k]
                e2[k] = t

            #mutation
            if random.randint(0, 100) < mutation * 100:
                e1[k] = random.uniform(-bound, bound)
            if random.randint(0, 100) < mutation * 100:
                e2[k] = random.uniform(-bound, bound)

        new_population.append(e1)
        new_population.append(e2)

    population = new_population
