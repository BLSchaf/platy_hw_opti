import os, csv
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import Tk

Tk().withdraw()


path = os.getcwd()
path = path.replace('\\', '/')
print(path)
    
filename = askopenfilename(initialdir = '{}/__database__'.format(path),
                           title = 'Select *.csv'
                           )
i = []
with open ('{0}'.format(filename),
           newline = '') as ifile:
    
    reader = csv.reader(ifile, delimiter=',')
    header = next(reader)
    
    for row in reader:    
        #individuals[Nachgiebigkeit, Ähnlichkeit, Herkunft, Inidividuum, Parameter]
        i.append([row[0],
                  row[1],
                  float(row[2]),
                  float(row[3]),
                  row[4][1:-1].split(',')
                  ])


params = []
p = 4
for n in range(len(i)):
    params.append(list(map(int,i[n][4])))
    
makros = [params[i:i+p] for i in range(0, len(params), p)]
print(params[0],makros[0])

print(params)
params_h = []
params_n = []
for n in params:
    if n[0] == 2:
        params_h.append(n)
    else:
        params_n.append(n)
print(params_h)
        


#plt.axvline(x = 1, linestyle = '--', c = 'black', alpha = 0.5)

x = [r[1] for r in params_h]
y = [r[2] for r in params_h]
z = [r[3]**3 for r in params_h]

plt.scatter(x, y, s=z, alpha=0.4, edgecolor='grey', label = 'hole')

x = [r[1] for r in params_n]
y = [r[2] for r in params_n]
z = [r[3]**3 for r in params_n]
plt.scatter(x, y, s=z, alpha=0.4, edgecolor='grey', label= 'nondesign')
    
plt.xlim(0, 120)
plt.ylim(0, 80)

plt.xlabel('X-Koordinate [mm]')
plt.ylabel('Y-Koordinate [mm]')

lgnd = plt.legend(loc="lower left", scatterpoints=1, fontsize=10)
lgnd.legendHandles[0]._sizes = [60]
lgnd.legendHandles[1]._sizes = [60]

plt.show()
