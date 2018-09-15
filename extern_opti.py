from platypus import NSGAII, NSGAIII, SPEA2, EpsMOEA, IBEA, Problem
from __extern_opti__ import variable_range as var
from intern_opti import intern_opti
import time


def extern_opti(n, p, o, xmax, ymax, pop_size, iterations):
    
    # Festlegen des Optimierungsproblems (Variablen, Ziele)
    problem = Problem(n*p, o)


    # Festlegen der Parametergrenzen (problem.types)
    problem.types = var.param_values(problem, n, p, o, xmax, ymax)


    # Übergabe der internen Berechnungen
    problem.function = intern_opti


    # Auswahl des externen Algorithmus und dessen Variablen
    algorithm = NSGAII(problem,
                       population_size = pop_size)


    # Start des externen Algorithmus -
    algorithm.run(iterations)

    print(' Optimization complete!\n', time.strftime(' %d.%m.%Y %H:%M:%S'))

    print('Results stored')

