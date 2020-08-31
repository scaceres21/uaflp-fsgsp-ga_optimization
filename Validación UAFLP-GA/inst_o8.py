# Python Script para la optimización de UAFLP mediante GA (Instancias Meller et al 8 dptos)

from algGenetico_uaflp import *
import pandas as pd


# Extraer y preparar datos de entrada de 'inst_o8.xlsx'

data = pd.read_excel("inst_o8.xlsx")

# Flujos de materiales * Costos de manejo
flujos_cols = list(data.columns.values)
flujos_mats = np.array(data[flujos_cols[1:9]])

# Tamaño de la instalación y dimensiones de áreas
dim_instalacion = list(data["Facility"][0:2])
areas_depts = np.array(data["Area"])


# Crear clase Layout con las características de la instalación

layout = Layout(num_depts=len(areas_depts), areas_depts=areas_depts, lados_instal=dim_instalacion,
                rel_aspecto_max=4, flujos_materiales=flujos_mats)


# Try best Palomo-Romero (2017)

# cromo_dep = np.array([7, 4, 1, 2, 3, 6, 8, 5])
# cromo_bay = np.array([0, 0, 0, 1, 0, 0, 0, 1])

# Try best García-Hernández (2020)

# cromo_dep = np.array([5, 8, 6, 3, 2, 1, 4, 7])
# cromo_bay = np.array([0, 0, 0, 1, 0, 0, 0, 1])

# fitness = layout.fitness(cromo_dep, cromo_bay)
# layout.mostrar_layout(cromo_dep, cromo_bay)


# Crear clase AlgGenetico con los parámetros del algoritmo genético

ga = AlgGenetico(tam_poblacion=100, num_generaciones=200, tam_torneo=2, prob_cruce=0.9, prob_mutacion=0.1)


# Aplicación del algoritmo genético para la instancia dada

reps = 0
best_rep = []
best_ind_rep = []

while reps < 10:

    # Determinar población inicial y función fitness de la población inicial
    poblacion = ga.poblacion_inicial(layout)
    best, best_individuo = ga.obtener_mejor(layout, poblacion)

    fit_gen = []
    individuos_min = []
    generaciones = 0

    while generaciones < ga.num_generaciones:

        for t in range(int(ga.tam_poblacion / 2)):

            # Seleccionar individuos padre para cruce mediante torneo de selección
            padres = ga.seleccion(layout, poblacion)
            parents = padres.copy()

            # Cruzar los dos individuos seleccionados mediante método partially matched crossover (PMX)
            children = ga.cruce(layout, parents)

            # Mutar los nuevos individuos hijos cruzados
            children = ga.mutacion(layout, children)

            # Sustituir los nuevos individuos por los peores individuos de la población actual
            poblacion = ga.sustitucion(layout, poblacion, children)

        print(poblacion)

        # Obtener el mejor individuo de la generación

        best, best_individuo = ga.obtener_mejor(layout, poblacion)

        # Guardar mejor individuo de la generación

        fit_gen.append(best)
        individuos_min.append(best_individuo)
        print("Generación n°: ", generaciones)

        # Pasar a la siguiente generación

        generaciones += 1

    best_rep.append(min(fit_gen))
    p_min = fit_gen.index(min(fit_gen))
    best_ind_rep.append(individuos_min[p_min])
    reps += 1

df = pd.DataFrame(best_rep)
df.to_excel("results_O8.xlsx")

# Hallar el mejor individuo y su fitness de todas las generaciones
# print(fit_gen)
# print(individuos_min)
# fit_best = min(fit_gen)
# pos_fit_best = fit_gen.index(fit_best)

# Mostrar el layout del mejor individuo y su fitness
# layout.mostrar_layout(individuos_min[pos_fit_best][0], individuos_min[pos_fit_best][1])

# Mostrar el plot generaciones vs mejor fitness
# plt.plot(list(range(ga.num_generaciones)), fit_gen)
# plt.show()
