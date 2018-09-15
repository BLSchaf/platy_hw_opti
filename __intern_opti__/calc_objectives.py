import os
from .extract_comps import extract_comp_origin, extract_comp_new
from .extract_similarity import compare_dens

def calc_objectives(original_sh, original_hgdata, path_temp):    
    '''Berechnet die Zielfunktion'''
    
    # Objective 1: get compliance
    comp_origin = extract_comp_origin(original_hgdata)
    comp_new = extract_comp_new(path_temp)    
    
    # Expression w_comp (weight factor)
    w_comp = 1

    # objective_1 normalized
    objective_1 = w_comp * comp_new/comp_origin
    objective_1 = round(objective_1, 6)
    
#--------------------------------------------------------------------------

    
    # Objective 2: get similarity
    similarity = compare_dens(original_sh, path_temp)
            
    # Expression w_similarity (weight factor)
    w_similarity = 1
            
    # objective_2 penalized and normailized
    if objective_1 >= 1000:
        objective_2 = w_similarity * similarity + 1000
    else:
        objective_2 = w_similarity * similarity
    objective_2 = round(objective_2, 6)
    
      
    # Calculate objective for single Objective Optimization
    fitness = objective_1 + objective_2
    fitness = round(fitness, 3)

    print ('\n============================\n Calculated Objectives')
    print ('obj1:',objective_1, '\nobj2:',objective_2, '\nobjT:', fitness)

    return objective_1, objective_2, fitness
