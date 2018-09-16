import os, csv
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import Tk

Tk().withdraw()


path = os.getcwd()
path = path.replace('\\', '/')
print(path)
    
filename = askopenfilename(initialdir = '{}/__database__'.format(os.path.dirname(path)),
                           title = 'Select *.csv'
                           )
ind = []
with open ('{0}'.format(filename),
           newline = '') as ifile:
    
    reader = csv.reader(ifile, delimiter=',')
    header = next(reader)
    
    for row in reader:    
        #individuals[Nachgiebigkeit, Ähnlichkeit, Herkunft, Inidividuum, Parameter]
        ind.append([row[0],
                  row[1],
                  float(row[2]),
                  float(row[3]),
                  row[4][1:-1].split(',')
                  ])


params = []
p = 4
for n in range(len(ind)):
    params.append(list(map(int,ind[n][4])))

print(params[0])

makros = []
for v in params:          
    makros.append([v[i:i+p] for i in range(0, len(v), p)])
    
print(makros[0])

makro_h = []
makro_n = []

for ind in makros:
    for makro in ind:
        
        if makro[0] == 2:
            makro_h.append(makro)
        else:
            makro_n.append(makro)
            
print (makro_h[0])
            
x = [r[1] for r in makro_h]
y = [r[2] for r in makro_h]
z = [r[3]**3 for r in makro_h]

plt.scatter(x, y, s=z, alpha=0.4, edgecolor='grey', label = 'hole')

x = [r[1] for r in makro_n]
y = [r[2] for r in makro_n]
z = [r[3]**3 for r in makro_n]
plt.scatter(x, y, s=z, alpha=0.4, edgecolor='grey', label= 'nondesign')
    
plt.xlim(0, 120)
plt.ylim(0, 80)

plt.xlabel('X-Koordinate [mm]')
plt.ylabel('Y-Koordinate [mm]')

lgnd = plt.legend(loc="best", scatterpoints=1, fontsize=10)
lgnd.legendHandles[0]._sizes = [60]
lgnd.legendHandles[1]._sizes = [60]

filesave = ('.').join(filename.split('.')[:-1])
plt.savefig('{0}_position_makro.pdf'.format(filesave),
            bbox_inches='tight')
plt.show()
