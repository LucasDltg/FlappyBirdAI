import numpy as np


def sigmoid(x):
    return 1/(1+np.exp(-x))


def process(deltax, deltay, yspeed, weight):
    #normalise input
    A = deltax
    B = deltay
    C = yspeed
    #neuronal calcul
    D = A*weight[0]+B*weight[1]+C*weight[2]+weight[3]
    D = sigmoid(D)
    E = A*weight[4]+B*weight[5]+C*weight[6]+weight[7]
    E = sigmoid(E)
    F = D*weight[8]+E*weight[9]+weight[10]
    F = sigmoid(F)
    if F > 0.5:
        return True
    return False

