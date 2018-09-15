import subprocess, time, os, shutil

def take_pic_origin(original_h3d, path,name_db, path_hw):
    '''Erstellt Tcl-Skript für Bildaufnahme der Originallösung'''
    
    start_time_take_pic = time.clock()
    print ('\n============================\n Taking Picture of Original Solution')

    take_pic = '''
hwi GetSessionHandle Session1
	Session1 GetProjectHandle Project1
		Project1 GetPageHandle Page1 1
			Page1 GetWindowHandle Win1 1
				Win1 GetClientHandle Client1
					# Model wird geladen
					Client1 AddModel "{0}"
					Client1 GetModelHandle Model1 1
						Model1 SetResult "{0}"
						Model1 GetResultCtrlHandle Result1
							# Auf letzte Iteration setzen
							set GeNuSi1 [Result1 GetNumberOfSimulations 1]
							set GeNuSi2 [expr $GeNuSi1 - 1]
							Result1 SetCurrentSimulation $GeNuSi2
							Result1 GetContourCtrlHandle Contour1 1
								# Contour-Ergebnisse darstellen
								Contour1 SetEnableState true
								Contour1 ReleaseHandle
							Result1 ReleaseHandle
						Model1 ReleaseHandle
					Client1 ReleaseHandle
				Win1 GetViewControlHandle ViewControl1
					# Model ausrichten
					ViewControl1 SetOrientation 1 0 0
					ViewControl1 Fit
					ViewControl1 ReleaseHandle
 				Win1 ReleaseHandle
 			Page1 ReleaseHandle
 		Project1 ReleaseHandle
	# Arbeitsfenster in TIFF ausgeben
	Session1 CaptureActiveWindow TIFF "Original.tif" pixels 1024 768
 	Session1 ReleaseHandle'''.format(original_h3d)
    
    with open ('take_pic.tcl' , 'w') as ofile:
        print(take_pic, file=ofile)
        
    subprocess.run('{}/hw/bin/win64/hw.exe /clientconfig hwpost.dat -b -tcl {}/take_pic.tcl'.format(path_hw, path))

    t = 0
    while not os.path.exists('{}/Original.tif'.format(path)):
        time.sleep(1)
        t += 1
        if t > 300:
            print('Something went wrong while taking the screenshot\
of the original solution Hyperworks')
            break
        
    if os.path.isfile('{}/Original.tif'.format(path)):
        shutil.move('{}/Original.tif'.format(path), '{}/Original.tif'.format(name_db))
        time_take_pic = time.clock() - start_time_take_pic
        
        print('\n Hyperview: --- {:2.0f} seconds --- \n\
Picture Stored'.format(time_take_pic))
