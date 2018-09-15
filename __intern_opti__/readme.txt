Enthält alle Module des internen Optimierungsprozesses

__init__.py		- __intern_opti__ als Package deklarieren

makro.py 		- Injizieren der Makrostrukturen und starten der Topologieoptimierung

calc_objective.py 	- Auswerten der Outputdateien von OptiStruct
	extract_comps.py	- Auslesen der Nachgiebigkeit
	extract_similarity.py 	- Auswerten der Ähnlichkeit

take_pic 		- Aufnahme eines Screenshots der Lösung

Um die Masse der Topologieoptimierung zu variieren:
*setvalue opticonstraints id=1 STATUS=1 upperbound=0.4
