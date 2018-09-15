from platypus import Problem, Integer

def param_values(problem, n, p, o, xmax, ymax):
    ''' Festlegen der Parametergrenzen '''

    # Erstellen einer Liste der Bereichsgrenzen für die Makros
    divide = []
    if xmax >= ymax:
        for i in range(0, n+1):
            if i == 0:
                d =  11
                divide.append(d)
            else:
                d = int(i*(xmax-14)/n)+11
                divide.append(d)
    else:
        for i in range(0, n+1):
            d = int(i*(ymax)/n)
            divide.append(d)
            
    divideD = [divide[i:i+2] for i  in range(0, n)]
    position = 0 # Laufvariable für divideD
    
    
    # Festlegen der Parametergrenzen je Parametertyp        
    for i in range(0, n*p):
        
        # Parameter für Art des Makro
        if i % p == 0:
            problem.types[i] = Integer(1, 2)
        # Parameter für Radius
        elif i % p == 3:
            problem.types[i] = Integer(2, 8)
        # Parameter für X- und Y-Koordinaten des Makro
        else:
            if xmax >= ymax:
                
                if i % p == 1:
                    problem.types[i] = Integer(divideD[position][0],
                                               divideD[position][1]-8)
                    position += 1
                else:
                    problem.types[i] = Integer(0, ymax)
                    
            else:
                if i % p == 1:
                    problem.types[i] = Integer(0, xmax)
                else:
                    problem.types[i] = Integer(divideD[position][0],
                                               divideD[position][1]-8)
                    position += 1
    print ('============================\n Set problem.types:\n ',
           *problem.types, sep='\n ')
    
    return (problem.types)

