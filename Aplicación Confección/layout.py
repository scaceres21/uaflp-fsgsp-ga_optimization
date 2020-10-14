# Creación del objeto Layout

import numpy as np
import math
import matplotlib.pyplot as plt


class Layout:

    # Método 0. Constructor de problema de Facility Layout

    def __init__(self, num_depts, areas_depts, lados_instal,
                 flujos_materiales=None, costos_manejo=1, rel_aspecto_max=5,
                 param_sever_k=3, euclidean=False, nom_depts=False):

        # Parámetros de entrada

        self.num_depts = num_depts
        self.areas_depts = areas_depts
        self.lados_instal = lados_instal
        self.flujos_materiales = flujos_materiales
        self.costos_manejo = costos_manejo
        self.rel_aspecto_max = rel_aspecto_max
        self.param_sever_k = param_sever_k
        self.euclidean = euclidean
        self.nom_depts = nom_depts

        # Comprobaciones:

        # area_total = self.lados_instal[0] * self.lados_instal[1]
        # if sum(self.areas_depts) <= area_total:
        #     print("Requerimientos de área: OK")
        # else:
        #     print("Warning: área de departamentos > área total")
        #     exit()

        # Creación automática de matriz de flujos en caso de "None"

        if self.flujos_materiales is None:
            comb = math.factorial(self.num_depts) / (math.factorial(2) * math.factorial(self.num_depts - 2))
            self.flujos_materiales = np.random.randint(0, 100, int(comb))

    # Método 1. Mostrar por pantalla los atributos actuales de la clase

    def obtener_atributos(self):
        print("\nATRIBUTOS DE LA CLASE:\n"
              "Número de departamentos: {}\n"
              "Áreas de los departamentos: {}\n"
              "Dimensiones de la instalación: {}\n"
              "Flujos entre departamentos: \n {}\n"
              "Costos por unidad de manejo:\n {}\n"
              "Relación de aspecto máxima de departamentos: {}\n"
              "Parámetro de severidad de la penalización (k): {}\n"
              "Norma de la distancia euclideana: {}\n"
              "Nombre de los departamentos: {}".format(self.num_depts,
                                                       self.areas_depts,
                                                       self.lados_instal,
                                                       self.flujos_materiales,
                                                       self.costos_manejo,
                                                       self.rel_aspecto_max,
                                                       self.param_sever_k,
                                                       self.euclidean,
                                                       self.nom_depts))

    # Método 2. Definir los nuevos valores de los atributos de la clase

    def modificar_atributos(self, num_depts, areas_depts, lados_instal,
                            flujos_materiales=None, costos_manejo=1, rel_aspecto_max=5,
                            param_sever_k=3):
        self.num_depts = num_depts
        self.areas_depts = areas_depts
        self.lados_instal = lados_instal
        self.flujos_materiales = flujos_materiales
        self.costos_manejo = costos_manejo
        self.rel_aspecto_max = rel_aspecto_max
        self.param_sever_k = param_sever_k

        # Comprobaciones:
        # area_total = self.lados_instal[0] * self.lados_instal[1]
        # if sum(self.areas_depts) <= area_total:
        #     print("Requerimientos de área: OK")
        # else:
        #     print("Warning: área de departamentos > área total")
        #     exit()

        # Creación automática de matriz de flujos en caso de "None"
        if self.flujos_materiales is None:
            comb = math.factorial(self.num_depts) / (math.factorial(2) * math.factorial(self.num_depts - 2))
            self.flujos_materiales = np.random.randint(0, 100, int(comb))

    # Método 3. Decodificar cromosomas de departamentos y de bahías

    def decodificar_fbs(self, cromo_depts, cromo_bahias):

        # 3.0 Crear estructuras necesarias para el método

        # Lista para obtener la posición de las bahías
        bays = []
        # Lista para ingresar las áreas de cada bahía
        areas_bays = []
        # Lista para agregar los departamentos en cada bahía
        depts_bays = []
        # Arrays de ceros para ingresar las dimensiones de los lados y centroides de los deptos
        lados = np.zeros(self.num_depts, dtype=np.ndarray)
        centroides = np.zeros(self.num_depts, dtype=np.ndarray)

        # 3.1 Identificar las posiciones en que se parten las bahías

        for ind_k in range(len(cromo_bahias)):
            k = cromo_bahias[ind_k]
            if k == 1:
                bays.append(ind_k)

        # print("\nPosiciones de las bahías: {}".format(bays))

        # 3.2 Determinar los departamentos pertenecientes a cada bahía
        suma_depts = 0
        depts = []
        for j in range(len(cromo_depts)):
            i = cromo_depts[j]
            if j in bays:
                suma_depts += self.areas_depts[i - 1]
                areas_bays.append(suma_depts)
                suma_depts = 0
                depts.append(i)
                depts_bays.append(depts)
                depts = []
            else:
                suma_depts += self.areas_depts[i - 1]
                depts.append(i)

        # print("Áreas de las bahías: {}\n"
        #      "Departamentos en cada bahía: {}".format(areas_bays,
        #                                               depts_bays))

        # 3.3 Determinar el ancho de las bahías, y las dimensiones y
        # centroides de los departamentos

        contador_ancho = 0
        for ind_a in range(len(areas_bays)):
            a = areas_bays[ind_a]
            ancho_bay = a / self.lados_instal[1]
            contador_alto = 0
            for b in depts_bays[ind_a]:
                alto_dep = self.areas_depts[b - 1] / ancho_bay
                lados[b - 1] = [ancho_bay, alto_dep]
                x = contador_ancho + ancho_bay / 2
                y = contador_alto + alto_dep / 2
                centroides[b - 1] = [x, y]
                contador_alto += alto_dep
            contador_ancho += ancho_bay

        return lados, centroides

    # Método 4. Determinar la fitness function de un individuo dado

    def fitness(self, cromo_depts, cromo_bahias):

        # 4.0 Crear estructuras necesarias para el método

        departamentos = np.arange(1, self.num_depts + 1)
        # Matriz de ceros para agregar distancias y flujos entre departamentos
        distancias = np.zeros((self.num_depts, self.num_depts))

        # 4.1 Decodificar cromosomas de departamentos y de bahías

        lados_depts, centros_depts = self.decodificar_fbs(cromo_depts, cromo_bahias)

        # # Crear matriz de flujos entre departamentos

        # indice_flujos = 0
        # for i in range(len(departamentos)):
        #     for j in departamentos[i + 1:]:
        #         j = list(departamentos).index(j)
        #         flujos_materiales[j, i] = self.vector_flujos[indice_flujos]
        #         indice_flujos += 1

        # print("\nMatriz de flujos entre departamentos: \n{}".format(flujos_materiales))

        # 4.2 Crear matriz de distancias rectilíneas/euclideanas entre departamentos

        if self.euclidean is True:

            for k in range(len(departamentos)):
                for d in departamentos[k + 1:]:
                    d = list(departamentos).index(d)
                    distancias[d, k] = math.sqrt(((centros_depts[k][0] - centros_depts[d][0]) ** 2) +
                                                 ((centros_depts[k][1] - centros_depts[d][1]) ** 2))
        else:
            for k in range(len(departamentos)):
                for d in departamentos[k + 1:]:
                    d = list(departamentos).index(d)
                    distancias[d, k] = math.fabs(centros_depts[k][0] - centros_depts[d][0]) + \
                                       math.fabs(centros_depts[k][1] - centros_depts[d][1])

                    # print("Matriz de distancias rectilíneas entre departamentos: \n{}".format(distancias))

        # 4.3 Calcular los costos por manejo de materiales MHC = Costo * Flujos * Distancias

        costo_manejo_mat = np.sum(self.costos_manejo * self.flujos_materiales * distancias)

        # print("Costo por manejo de materiales obtenido: {}".format(costo_manejo_mat))

        # 4.4 Definir la función de ajuste (fitness) para el layout decodificado
        # fitness(x) = MHC(x) + MHC(x) * (nx) ** k,
        # donde, x: layout, nx: num. departamentos no factibles,
        # k: parámetro de severidad = 3 (Tate-Smith, 1995), MHC: Costo de manejo de materiales

        num_nofactibles = 0
        for i in cromo_depts:
            aspect_ratio = max(lados_depts[i - 1][0], lados_depts[i - 1][1]) / min(lados_depts[i - 1][0],
                                                                                   lados_depts[i - 1][1])
            if aspect_ratio > self.rel_aspecto_max:
                num_nofactibles += 1

        # print("Número de instalaciones no factibles: ", num_nofactibles)

        fit = costo_manejo_mat + costo_manejo_mat * (num_nofactibles ** self.param_sever_k)

        return fit

    # Método 5. Mostrar layout de planta decodificado

    def mostrar_layout(self, cromo_depts, cromo_bahias):

        # 5.1 Colores de los departamentos

        # cols = np.array(["red", "green", "yellow", "orange", "blue", "brown", "grey", "beige",
        #                 "azure", "coral", "crimson", "gold", "indigo", "magenta", "sienna",
        #                 "whitesmoke", "indianred", "darkcyan", "mediumseagreen", "olivedrab"])
        # colores_dptos = cols[:self.num_depts]
        names = self.nom_depts

        # 5.2 Decodificar cromosomas de departamentos y de bahías

        lados_depts, centros_depts = self.decodificar_fbs(cromo_depts, cromo_bahias)

        # 5.3 Crear figura, subplot y establecer los límites del gráfico

        fig = plt.figure(dpi=300, figsize=(4, 6))
        plt.rcParams.update({'font.size': 6})
        ax = fig.add_subplot(111)
        ax.set_xlim([0, self.lados_instal[0]])
        ax.set_ylim([0, self.lados_instal[1]])

        # 5.3 Crear gráfico de acuerdo con posición y lados de departamentos

        for i in range(len(centros_depts)):
            esquina_inicio = centros_depts[i] - np.divide(lados_depts[i], 2)
            rect = plt.Rectangle(esquina_inicio, width=lados_depts[i][0],
                                 height=lados_depts[i][1], facecolor="white",
                                 edgecolor="black")
            plt.text(centros_depts[i][0], centros_depts[i][1], "{}".format(names[i]),
                     horizontalalignment="center",
                     verticalalignment="top")
            # centros_depts[i][0],
            # centros_depts[i][1]),

            plt.plot(centros_depts[i][0], centros_depts[i][1], color="black", marker=None, markersize=2)
            plt.gca().add_patch(rect)

        plt.show()
        plt.savefig("layout.png")
