# Código para la optimización de la programación de la producción integrando decisiones de distribución de planta para el caso del sector de la confección 

## Carpeta: Validación UAFLP-GA

Esta carpeta contiene el código relacionado con la validación del algoritmo genético (GA) en las instancias del problema de distribución de plantas con áreas desiguales (unequal-area facility layout problem, UAFLP).

Esta carpeta incluye:

* algGenetico_ualfp.py: Este archivo contiene la clase en donde se definen los operadores del GA para el UAFLP
* layout: Este archivo contiene la clase en donde se decodifica el cromosoma del GA para la obtención de los departamentos de la planta, se calcula la función fitness y se muestra el layout
* inst_....py: Hace referencia a las instancias de datos evaluadas para el problema: O7, O8, O9, vC10Ra y MB12
* Archivos .xlsx: Archivos de excel que contienen los datos de las instancias evaluadas

## Carpeta: Validación FSGSP-GA

Esta carpeta contiene el código relacionado con la validación del algoritmo genético (GA) para el problema de programación de la producción en celdas de manufactur flowshop (flowshop group scheduling problem, FSGSP).

Esta carpeta incluye:

* algGeneticoSched.py: Este archivo contiene la clase en donde se definen los operadores del GA para el FSGSP
* group_scheduling.py: Este archivo contiene la clase en donde se decodifica el cromosoma del GA para la obtención de la secuencia de familias y de trabajos en cada familia, se calcula la función objetivo (makespan, total completion time o total weighted tardiness) y se obtienen los valores óptimos mediante el módulo PuLP
* fsgsp_....py: Estos archivos comprenden la aplicación del GA a las instancias de datos propuestas por Salmasi et al, 2010, para 2 (2m), 3 (3m) y 6 (6m) máquinas, así como para la optimización del tiempo de terminación total (tct) y de la tardanza ponderada total (twt).

## Carpeta: Aplicación Confección

Esta carpeta incluye el código utilizado para la aplicación del algoritmo genético al caso del sector de la confección de prendas de vestir de la ciudad de Cúcuta: empresa de confección de ropa deportiva. 

Esta carpeta incluye:

* layout, group_scheduling, algGenetico_uaflp, algGeneticoSched: Archivos anteriormente mencionados que definen las clases para los problemas UAFLP, FSGSP y para el GA.
* uaflp_fsgsp_confeccion_mhc_twt.py:  Este archivo llama a las clases para aplicar el GA a los problemas UAFLP y FSGSP para el caso de estudio, así como los datos de entrada para cada problema. En este archivo, el GA optimiza estos problemas para obtener el menor costo de manejo de materiales (MHC) y penalización por tardanza de los trabajos (TWT).
* layout_actual.py: En este archivo se calcula el MHC para el estado actual del caso de confección.
* scheduling_actual.py: En este archivo se calcula el TWT para el estado actual del caso de confección.
* fsgsp_confeccion_cmax/tct.py: En este archivo se aplica el GA para solucionar el FSGSP para el estado propuesto, con el fin de minimizar el makespan (Cmax) y el tiempo total de terminación (TCT).
* Layout_Actual.png, Layout_Best.png, Layout_Propuesto_iter1.png: Imágenes del layout de bloques para la situación actual, el mejor encontrado por el GA y el layout propuesto para el caso del sector de la confección, respectivamente.
* Input_....xlsx: Archivos que contienen los datos de entrada para el GA, tanto para el estado actual como para el estado propuesto.

## Carpeta: Simulación en Simio

Esta carpeta incluye archivo .md que contiene el link para acceder al modelo de simulación en Simio y al diseño de planta actual y propuesta en SketchUp
