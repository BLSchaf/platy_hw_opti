import os, time
import shutil


def extract_dens_origin(original_sh):
    '''Ermittelt Dichtewert der Elemente der Ursprungsdatei'''

    element_origin = []
    dens_origin = []
    with open('{}'.format(original_sh), 'r')  as ifile:
        lines = ifile.readlines()[2:]
        for i, dens in enumerate(lines):
            if i % 2 != 0:
                dens_origin.append(float(dens))                
            else:
                j = dens.split()
                if len(j)> 2:
                        break
                element_origin.append(int(j[0]))
                
    return element_origin, dens_origin
                

def extract_dens_new(path_temp):
    '''Ermittelt Dichtewert der Elemente des aktuellen Individuums'''

    element_new = []
    dens_new = []  
    with open('{}.sh'.format(path_temp), 'r')  as ifile:
        lines = ifile.readlines()[2:]
        for i, dens in enumerate(lines):
            if i % 2 != 0:
                 dens_new.append(float(dens))
            else:
                j = dens.split()
                if len(j)> 2:
                        break
                element_new.append(int(j[0]))
        
    return element_new, dens_new 


def compare_dens(original_sh,path_temp):
    '''Vergleicht die Dichtewerte der Elemente
    von Ursprungsdatei und aktuellem Individuum
    '''

    element_origin, dens_origin = extract_dens_origin(original_sh)
    element_new, dens_new = extract_dens_new(path_temp)

    lines_fem = []
    with open('{}.fem'.format(path_temp), 'r') as ifile:
        for line in ifile:
            if line.startswith("CQUAD4"):
                lines_fem.append(int(line.split()[1]))
    
    delta = 0
    j = 0
    
    for i,_ in enumerate(element_origin):

        try:
            if  element_origin[i] == element_new[j]:
                delta = delta + abs(dens_new[j] - dens_origin[i])
                j += 1
                
            elif element_origin[i] in lines_fem:
                #print ('element_new in .fem but not found in .sh', element_origin[i], 'next element_new', element_new[j])
                delta = delta + 1 - dens_origin[i]
                
            elif element_origin[i] not in lines_fem:
                #print ('element_new not in .fem: +',element_origin[i], dens_origin[i])
                delta = delta + dens_origin[i]
                      
            else:
                # dens_new[j] < dens_origin[i]:
                #print (element_new[j], element_origin[i], 'Error in original model: Element is missing')
                break
            
        except IndexError:
            if element_origin[i] in lines_fem:
                print ('element_new in .fem but not found in .sh',
                       element_origin[i],
                       'next element_new not existing'
                       )
                
                delta = delta + 1 - dens_origin[i]
                
            else:
                print ('element_new not in .fem: +',element_origin[i], dens_origin[i])
                delta = delta + dens_origin[i]
                      
            
    sigma = 1 - (delta/len(element_origin))
    sigma = round(sigma, 3)

    return sigma
