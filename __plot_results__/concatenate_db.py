import csv, os
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename as asaf,
askdirectory as askdir
from tkinter import Tk

Tk().withdraw()


def concatenate_databases():
    '''Verketten ausgewählter Dataenbanken'''

    path = os.getcwd()
    path = path.replace('\\', '/')

    dirs = []
    title = 'Choose directories'
    while True:
        dir = askdir(initialdir = '{}/__database__'.format(path),
                                      title=title)
        if not dir:
            break
        
        dirs.append(dir)
        title = 'Got {}. Next dir...'.format(dirs[-1].split('/')[-1])


    new_database = asaf(initialdir = '{}/__database__'.format(path),
                        title = 'Save Databse as...',
                        filetypes = [("Csv File", "*.csv")]
                        )
    
    print('new_db', new_database)

    with open('{}.csv'.format(new_database),
              'a', newline = '') as ofile:
        
        fieldnames = ['Herkunft',
                      'Individual',
                      'Objective1 (Nachgiebigkeit)',
                      'Objective2 (Ähnlichkeit)',
                      'Params'
                      ]
        
        writer = csv.DictWriter(ofile, fieldnames = fieldnames)
        writer.writeheader()
        
        for dir in dirs:
            filename = dir.split('/')[-1]

            print('{0}/{1}.csv'.format(dir,filename))
            
            with open('{0}/{1}.csv'.format(dir,filename),
                      'r', newline = '') as ifile:
                
                reader = csv.reader(ifile, delimiter=',')
                next(reader)

                for row in reader:
                    writer.writerow({'Herkunft': filename,
                                     'Individual': row[1],
                                     'Objective1 (Nachgiebigkeit)': row[2],
                                     'Objective2 (Ähnlichkeit)': row[3],
                                     'Params': row[4]
                                     })
concatenate_databases()

