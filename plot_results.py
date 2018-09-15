from __plot_results__ import plot_functions
import os
from tkinter.filedialog import askopenfilename

def plot_results(filename, pop_size):
    '''Ausführen der Plotfunktionen'''

    print('Dateien in ', ('/').join(filename.split('/')[:-1]))
                          
    individuals = plot_functions.read_database(filename)

    nondominated = plot_functions.get_nondominated(individuals, filename)

    plot_functions.plot_nondominated(individuals, nondominated, filename)
    
    plot_functions.plot_convergence(individuals, filename, pop_size)


if __name__ == '__main__':
    '''Für die manuelle Ausführung'''
    
    path = os.getcwd()
    path = path.replace('\\', '/')
    print(path)
        
    filename = askopenfilename(initialdir = '{}/__database__'.format(path),
                               title = 'Select *.csv'
                               )
    pop_size = 20 #int(input('Population size: '))
    
    plot_results(filename)
