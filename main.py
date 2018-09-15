'''Starten des Optimierungsprozesses'''
import extern_opti as extern


# Parameter festelegen
xmax = 120
ymax = 80
n = 3
p = 4
o = 2
pop_size = 20
iterations = 600

# Pfad für Altair Hyperworks festlegen
path_hw = 'C:/Program Files/Altair/2017.2-edu'


if __name__ == '__main__':
    '''Starten des Externen Optimierungsprozesses'''
                    
    extern.extern_opti(n, p, o, xmax, ymax, pop_size, iterations)

    # Plot
    #...

    
