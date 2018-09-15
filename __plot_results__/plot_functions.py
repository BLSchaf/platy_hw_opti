import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter import Tk

Tk().withdraw()


def read_database(filename):
    '''Auslesen der Datenbank'''

    individuals = []
    failure = 0

    with open ('{0}'.format(filename),
               newline = '') as ifile:
        
        reader = csv.reader(ifile, delimiter=',')
        header = next(reader)
        
        for row in reader:
            if float(row[2]) <= 2:
                #individuals[Nachgiebigkeit, Ähnlichkeit, Herkunft, Inidividuum, Parameter]
                individuals.append([float(row[2]),
                                    float(row[3]),
                                    row[0],
                                    row[1],
                                    row[4],
                                    ])
            else:
                failure += 1

    print('Solutions unfeasable: ', failure)

    return individuals


def get_nondominated(individuals, filename):
    '''Bestimmen und Speichern der Pareto-optimalen Ergebnisse'''

    path = ('.').join(filename.split('.')[:-1])

    sorted_ind = sorted(individuals)
    nondominated = []
    for n,curr in enumerate(sorted_ind):

        prev = sorted_ind[0:n]
        
        if n == 0:
            nondominated.append(curr)
        
        elif curr[1] < (min(r[1] for r in prev)):
             nondominated.append(curr)
             

    with open ('{0}_nondominated.csv'.format(path),
               'w', newline = '') as ofile:
        
        fieldnames = ['Herkunft',
                      'Individual',
                      'Objective1',
                      'Objective2',
                      'Params'
                      ]
        
        writer = csv.DictWriter(ofile, fieldnames = fieldnames)
        writer.writeheader()
        
        for n in nondominated:
            writer.writerow({'Herkunft': n[2],
                             'Individual': n[3],
                             'Objective1': n[0],
                             'Objective2': n[1],
                             'Params': n[4]
                             })
             
    return nondominated

    
def plot_nondominated(individuals, nondominated, filename):
    '''Plotten aller Individuen
    und Hervorheben der Pareto-optimalen Individuen
    '''

    path = ('/').join(filename.split('/')[:-1])
    
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    
    plt.axvline(x = 1, linestyle = '--', c = 'black', alpha = 0.5)
    x = [r[0] for r in individuals]
    y = [r[1] for r in individuals]
    plt.scatter(x, y,
                s = 10,
                label = 'dominated',
                gid = 0)

    ndx = [n[0] for n in nondominated]
    ndy = [n[1] for n in nondominated]
    ndl = [n[3] for n in nondominated]
    plt.scatter(ndx, ndy,
                label = 'non-dominated',
                gid = 1)
    

    # Regression der nondominated Individuen
    z = np.polyfit(ndx, ndy, 3)
    p = np.poly1d(z)
    tg = np.linspace(min(ndx), max(ndx), 100)
    plt.plot(tg, p(tg), '--', c = 'xkcd:crimson',
             label = 'regr_nondominated',
             gid = 2)

    plt.xlim(min(x)*0.97, max(x)*1.03)
    plt.ylim(min(y)*0.97, max(y))

    plt.xlabel('$f_1([x])$ $Compliance$')
    plt.ylabel('$f_2([x])$ $Similarity$')
    
    plt.legend(loc='best')
    
    plt.savefig('{0}/results_pareto.pdf'.format(path),
                bbox_inches='tight')

    plt.xlim([min(ndx)*0.97, max(ndx)*1.03])
    plt.ylim([min(ndy)*0.97, max(ndy)*1.03])
    
    plt.savefig('{0}/zoomed_pareto.pdf'.format(path),
                bbox_inches='tight')
    
    #plt.show()


def plot_convergence(individuals, filename, pop_size):
    '''Plotten der Regression der dominierenden Lösungen je Generation'''

    path = ('/').join(filename.split('/')[:-1])

    individuals_gen = [individuals[gen:gen+pop_size+1]
                       for gen in range(0, len(individuals), pop_size)]
    
    plt.clf()
    
    #colormap = plt.cm.bwr
    #plt.gca().set_color_cycle([colormap(i)for i in np.linspace(0, 1, 30+2)])

    ax = plt.subplot(111)
    ax.set_prop_cycle('color',plt.cm.bwr(np.linspace(0, 1, 30+2)))
    
    for i,sorted_gen in enumerate(individuals_gen):
        sorted_gen = sorted(sorted_gen)
            
        nondominated_gen = []
        for n,ind in enumerate(sorted_gen):

            prev = sorted_gen[0:n]
        
            if n == 0:
                nondominated_gen.append(ind)
            
            elif ind[1] < (min(r[1] for r in prev)):
                nondominated_gen.append(ind)

        xgd = [g[0] for g in nondominated_gen]
        ygd = [g[1] for g in nondominated_gen]

        if len(nondominated_gen) <= 2:
            z = np.polyfit(xgd, ygd, 1)
        else:
            z = np.polyfit(xgd, ygd, 2)
            
        p = np.poly1d(z)
        tg = np.linspace(min(xgd), max(xgd), 100)

        if i % 5 == 0:
            plt.scatter(xgd, ygd)
            plt.plot(tg, p(tg), ':', label = 'regr-gen %s'%i)
        else:
            plt.plot(xgd, p(xgd), ':')


    plt.xlim(0.98, 1.05)
    plt.ylim(0.6, 1)

    plt.xlabel('$f_1([x])$ $Compliance$')
    plt.ylabel('$f_2([x])$ $Similarity$')
    
    plt.legend(loc='best')
    
    plt.savefig('{0}/results_conv.pdf'.format(path),
                bbox_inches='tight')
    #plt.show()
    
