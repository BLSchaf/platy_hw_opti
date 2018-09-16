import main as m
import os, time, shutil, csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
# Module für intern_opti(x) importieren
from __intern_opti__ import take_pic_origin, makro, calc_objectives, take_pic

Tk().withdraw()

'''Initialisieren der Laufvariablen, Pfade und Datenbank'''
    
global num
num = 0
global gen
gen = 1
global indv
indv = 0

#Vorbereiten der Pfade
print(time.strftime("%d.%m.%Y %H:%M:%S"))
print ('============================\n Set Population Size: ',
       m.pop_size, '\n')

# Pfad der Originaldateien und der neuen Individuen
path = os.getcwd()
path = path.replace('\\', '/')
print(path)

# Festlegen des Originalmodells
original_hm = askopenfilename(initialdir = '{}/__hw_origin__'.format(path),
                              title = 'Select Original Model'
                                  )

original_sh = (original_hm.split('.')[0]) + '.sh'
original_fem = (original_hm.split('.')[0]) + '.fem'
original_hgdata = (original_hm.split('.')[0]) + '.hgdata'
original_h3d  = (original_hm.split('.')[0]) + '_des' + '.h3d'

path_new = path+'/temp'

# Anlegen der Datenbank
path_db = path + '/__database__'

name_db = asksaveasfilename(initialdir = '{}'.format(path_db),
                            title = 'Save Databse as...',
                            filetypes = [("Csv File", "*.csv")]
                            )

print (' Path of Database:\n', name_db)

os.makedirs(name_db)

with open ('{}/{}.csv'.format(name_db, name_db.split('/')[-1]),
           'w', newline = '') as ofile:

        fieldnames = ['Algorithm',
                      'Individual',
                      'Objective1 (Nachgiebigkeit)',
                      'Objective2 (Ähnlichkeit)',
                      'Params'
                      ]
        
        writer = csv.DictWriter(ofile, fieldnames = fieldnames)
        writer.writeheader()

# Erstellen des Bildes der Originaldatei
take_pic_origin.take_pic_origin(original_h3d,
                                path,
                                name_db,
                                m.path_hw
                                )


def intern_opti(x):
    '''Steuern der internen Prozesse zur Topologieoptimierung
    - Rückgabewert sind die Zielfunktionen
    '''

    # Iterationsschritt der Laufvariablen
    global num
    num += 1
    global gen
    gen = (num-1) // m.pop_size
    global indv
    if gen == 0:
        indv = num
    else:
        indv = num -(m.pop_size*gen)
    
    print ('\n============================ New Individual {}.{} \
============================'.format(gen, indv))

    # Löschen alter Daten in jedem Iterationsschritt
    if os.path.isdir(path_new):
        shutil.rmtree(path_new)

    os.makedirs(path_new)

    
    # x[] in string für Dateinamen umwandeln    
    filename = ','.join(str(item) for item in x)
    path_temp = '/'.join([path_new, filename])

    print (' Individual Path:\n', path_temp)
    

    '''Tcl skript erzeugen und *.fem berechnen'''
    makro.optistruct_calc(x,
                          path,
                          original_hm,
                          path_temp,
                          m.path_hw,
                          m.p
                          )
     
    
    '''Objectives berechnen'''
    objectives = calc_objectives.calc_objectives(original_sh,
                                                original_hgdata,
                                                path_temp
                                                )
    

    '''Ergebnisse je Individuum in Datenbank schreiben'''
    with open ('{}/{}.csv'.format(name_db, name_db.split('/')[-1]),
               'a', newline = '') as ofile:
        
        writer = csv.DictWriter(ofile,
                            fieldnames = fieldnames)

        writer.writerow({'Algorithm': name_db.split('/')[-1],
                         'Individual': '.'.join([str(gen), str(indv)]),
                         'Objective1 (Nachgiebigkeit)': objectives[0],
                         'Objective2 (Ähnlichkeit)': objectives[1],
                         'Params': x
                         })
        
    '''Screenshot der Lösung nehmen'''
    take_pic.take_pic(path,
                      path_temp,
                      name_db,
                      gen,
                      indv,
                      m.path_hw
                      )

    '''Objectives an externen Algorithmus zurückgeben'''
    return objectives[0], objectives[1]
