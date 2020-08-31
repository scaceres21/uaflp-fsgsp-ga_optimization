# Código para la optimización de la programación de la producción integrando decisiones de distribución de planta para el caso del sector de la confección 

## Carpeta: Validación UAFLP-GA

Esta carpeta contiene el código relacionado con la validación del algoritmo genético (GA) en las instancias del problema de distribución de plantas con áreas desiguales (unequal-area facility layout problem, UAFLP).

Esta carpeta incluye:

* algGenetico_ualfp: Este archivo contiene la clase en donde se definen los operadores del GA para el UAFLP
* layout: Este archivo contiene la clase en donde se decodifica el cromosoma del GA para la obtención de los departamentos de la planta, se calcula la función fitness y se muestra el layout
* inst_...: Hace referencia a las instancias de datos evaluadas para el problema: O7, O8, O9, vC10Ra y MB12
* Archivos .xlsx: Archivos de excel que contienen los datos de las instancias evaluadas

## Carpeta: Validación FSGSP-GA

Esta carpeta contiene el código relacionado con la validación del algoritmo genético (GA) para el problema de programación de la producción en celdas de manufactur flowshop (flowshop group scheduling problem, FSGSP).

Esta carpeta incluye:
