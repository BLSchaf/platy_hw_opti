import os, time, subprocess, pprint

def optistruct_calc(x, path, original_hm, path_temp, path_hw, p):
    """ Überführt die Parameter x[] des Optimierungsalgorithmus
    in ein Tcl-Skript
    """

    # Array der Paramter interpretieren
    p = 4
    params = [x[i:i+p] for i  in range(0, len(x), p)]

    pp = pprint.PrettyPrinter()
    print ('\n Current Parameters:\n')
    pp.pprint(params)
    	

    # Platzhalter der Makrostrukturen auswählen
    makro = []
    for t, xv, yv, rv in params:
        if t == 1:
            makro.append('''\
*createmark elements 1 "by sphere" {} {} 0 {} "inside" 1 1 0
*movemark elements 1 "nonDesign"'''.format(xv, yv, rv))
        else :
            makro.append('''\
*createmark elements 1 "by sphere" {} {} 0 {} "inside" 1 1 0
*deletemark elements 1'''.format(xv, yv, rv))


    # Erzeugen des Tcl-scripts           
    optistruct ='''\
*readfile "{0}"
{1}
hm_answernext yes
*feoutputwithdata "{2}/templates/feoutput/optistruct/optistruct" \
"{3}.fem" 1 0 2 1 1
exec "{2}/hwsolvers/scripts/optistruct.bat" \
"{3}.fem" &
*quit 1 '''.format(original_hm, '\n'.join(makro), path_hw, path_temp)
   
    with open ('nonDesign.tcl' , 'w') as ofile:
        print(optistruct, file=ofile)


    # Erzeugen der *.fem und den damit ermittelten Ergebnissen
    print ('\n============================\n Running Optistruct')
    start_time_opti = time.clock()
    
    if os.path.isfile('{}.html'.format(path_temp)):
        os.remove('{}.html'.format(path_temp))
        
    # In der Studentenversion ist eine konsolenfreie Durchführng nicht möglich
    # Python 3.4 verwendet den den Syntax subprocess.run
    subprocess.call('{}/hw/bin/win64/hw.exe /clientconfig hwfepre.dat -tcl {}/nonDesign.tcl'.format(path_hw, path))
    #subprocess.run('{}/hm/bin/win64/hmbatch.exe -tcl {}/nonDesign.tcl'.format(path_hw, path)) 
    #subprocess.call('{}/hm/bin/win64/hmopengl.exe -batchmesher -noconsole -tcl {}/nonDesign.tcl'.format(path_hw, path))
    #subprocess.run('{}/hm/bin/win64/hmopengl.exe -batchmesher -noconsole -tcl {}/nonDesign.tcl'.format(path_hw, path))
    
    t = 0
    while not os.path.exists('{}.html'.format(path_temp)):
        time.sleep(1)
        t += 1
        if t > 300:
            print('Something went wrong while calling Hyperworks')
            break
   
    if os.path.isfile('{}.html'.format(path_temp)):
        time_opti = time.clock() - start_time_opti
        
        print('\n Optistruct took --- {:2.0f} seconds --- \n Output Ready for Evaluation '.format(time_opti))
