# Algoritmo genético para el UA-FLP

from layout import *


class AlgGenetico:

    # Método 0. Constructor con los parámetros de GA

    def __init__(self, tam_poblacion, num_generaciones, tam_torneo, prob_cruce, prob_mutacion):
        self.tam_poblacion = tam_poblacion
        self.num_generaciones = num_generaciones
        self.tam_torneo = tam_torneo
        self.prob_cruce = prob_cruce
        self.prob_mutacion = prob_mutacion

    # Método 1. Crear individuos de la población inicial

    def poblacion_inicial(self, layout):

        # 1.1 Estructuras necesarias para el método

        departamentos = np.arange(1, layout.num_depts + 1)
        poblacion = []

        # 1.2 Crear matriz con individuos de la población (departamentos y bahías)

        for p in range(self.tam_poblacion):
            individuo = []
            cromosoma_dep = np.random.permutation(departamentos)
            individuo.append(cromosoma_dep)

            cromosoma_bahias = []
            for casilla in range(len(departamentos) - 1):
                if np.random.rand() < 0.5:
                    cromosoma_bahias.append(0)
                else:
                    cromosoma_bahias.append(1)

            cromosoma_bahias.append(1)  # Siempre, el último departamento debe terminar en 1

            # Insertar individuos creados en la lista poblacion
            individuo.append(np.array(cromosoma_bahias))
            poblacion.append(individuo)

        poblacion = np.array(poblacion)
        print("Población de individuos: \n", poblacion)

        return poblacion

    # Método 2. Evaluar la función fitness y encontrar el mejor individuo de la población

    def obtener_mejor(self, layout, poblacion):

        best = 99999999
        best_ind = 0
        for ind in range(len(poblacion)):
            fitness_ind = layout.fitness(poblacion[ind, 0], poblacion[ind, 1])
            if fitness_ind < best:
                best = fitness_ind
                best_ind = poblacion[ind, :]

        print("El mejor individuo de la población es: \n", best_ind,
              "\nCon un valor de la función fitness de: \n", best)

        return best, best_ind

    # Método 3. Seleccionar individuos a cruzar según torneo

    def seleccion(self, layout, poblacion):

        # Tournament Selection

        ganador = 0
        ganador_pos = 999
        ganadores = []

        # 3.1 Elegir aleatoriamente individuos para el toreno

        ganador_torneo1 = 999
        for torneo in range(2):

            fit_ganador = 99999999
            pos_elegidas = []
            for k in range(self.tam_torneo):

                # Identificar posición aleatoria para participante
                pos = np.random.randint(0, len(poblacion), 1)[0]
                while pos in pos_elegidas or pos == ganador_torneo1:
                    pos = np.random.randint(0, len(poblacion), 1)[0]
                pos_elegidas.append(pos)

                # Actualizar el mejor del torneo
                fit_participante = layout.fitness(poblacion[pos, 0], poblacion[pos, 1])
                if fit_participante < fit_ganador:
                    fit_ganador = fit_participante
                    ganador = poblacion[pos, :]
                    ganador_pos = pos

            # Agregar al ganador del torneo a la lista ganadores
            ganadores.append(ganador)
            ganador_torneo1 = ganador_pos

        ganadores = np.array(ganadores)

        return ganadores

    # Método 4. Cruzar individuos seleccionados para generar nueva población

    def cruce(self, layout, padres):

        # Partially Matched Crossover (PMX)

        hijos = []

        # 4.1 Extraer individuos seleccionados como padres

        padre_dep1, padre_bay1 = padres[0, :]
        padre_dep2, padre_bay2 = padres[1, :]

        # 4.2 Evaluar probabilidad de cruce entre los padres

        if np.random.rand() <= self.prob_cruce:

            # 4.3 Encontrar posición de cortes para realizar cruce

            cortes = np.random.randint(0, layout.num_depts + 1, 2)
            cortes = np.sort(cortes)
            while cortes[0] == cortes[1] or len(range(cortes[0], cortes[1])) < 2:
                cortes = np.random.randint(0, layout.num_depts + 1, 2)
                cortes = np.sort(cortes)

            # 4.4 Realizar cruce de cromosomas de departamentos mediante PMX

            for i in range(cortes[0], cortes[1]):

                # Se identifican los genes en las posiciones de corte
                gen1 = padre_dep1[i]
                gen2 = padre_dep2[i]

                if gen1 != gen2:

                    # Se cambia el gen1 por el gen2 en los cromosomas de deptos
                    pos_g = 0
                    suma = 0
                    for g in padre_dep1:
                        if g == gen1:
                            padre_dep1[pos_g] = gen2
                            suma += 1
                        if g == gen2:
                            padre_dep1[pos_g] = gen1
                            suma += 1
                        pos_g += 1
                        if suma == 2:
                            suma = 0
                            break

                    pos_h = 0
                    for h in padre_dep2:
                        if h == gen1:
                            padre_dep2[pos_h] = gen2
                            suma += 1
                        if h == gen2:
                            padre_dep2[pos_h] = gen1
                            suma += 1
                        pos_h += 1
                        if suma == 2:
                            break

                # Se realiza cruce entre los dos puntos de corte para los cromosomas de bahías
                gen_bay1 = padre_bay1[i]
                gen_bay2 = padre_bay2[i]

                padre_bay1[i] = gen_bay2
                padre_bay2[i] = gen_bay1

        # 4.4 Añadir los individuos cruzados en la matriz nuevos_individuos

        hijo1 = []
        hijo2 = []
        hijo1.append(padre_dep1)
        hijo1.append(padre_bay1)
        hijo2.append(padre_dep2)
        hijo2.append(padre_bay2)

        hijos.append(hijo1)
        hijos.append(hijo2)
        hijos = np.array(hijos)

        return hijos

    # Método 5. Realizar mutación de individuos de acuerdo con operador de mutación

    def mutacion(self, layout, hijos):

        # 5.1 Evaluar la probabilidad de mutación de los dos hijos

        if np.random.rand() <= self.prob_mutacion:

            # 5.2 Mutar dos genes de los individuos hijos

            for ind_dep in hijos[:, 0]:

                # Por cada cromosoma de departamentos, se realiza un cambio entre 2 genes aleatorio
                genes = np.random.randint(0, layout.num_depts, 2)
                while genes[0] == genes[1]:
                    genes = np.random.randint(0, layout.num_depts, 2)

                gen1 = ind_dep[genes[0]]
                gen2 = ind_dep[genes[1]]

                ind_dep[genes[0]] = gen2
                ind_dep[genes[1]] = gen1

            # 5.2 Evaluar la probabilidad de mutación del cromosoma de bahías de los dos individuos

            for ind_bay in hijos[:, 1]:

                # Por cada cromosoma de bahías, se realiza un cambio entre 2 genes aleatorio

                genes = np.random.randint(0, layout.num_depts - 1, 2)  # Se omite el último gen, que debe ser siempre 1
                while genes[0] == genes[1]:
                    genes = np.random.randint(0, layout.num_depts - 1, 2)

                gen1 = ind_bay[genes[0]]
                gen2 = ind_bay[genes[1]]

                ind_bay[genes[0]] = gen2
                ind_bay[genes[1]] = gen1

        return hijos

    # Método 6. Sustituir los peores individuos de la población actual por los nuevos individuos

    def sustitucion(self, layout, poblacion, hijos):

        # 6.1 Evaluar la función fitness y eliminar los dos peores individuo

        for i in range(2):

            fit_peor = 0
            pos_peor = 999
            for ind in range(len(poblacion)):

                fit_ind = layout.fitness(poblacion[ind, 0], poblacion[ind, 1])

                if fit_ind > fit_peor:
                    fit_peor = fit_ind
                    pos_peor = ind

            poblacion = np.delete(poblacion, pos_peor, axis=0)

        # 6.2 Incluir los nuevos individuos a la población

        poblacion = np.append(poblacion, [hijos[0, :]], axis=0)
        poblacion = np.append(poblacion, [hijos[1, :]], axis=0)

        return poblacion
