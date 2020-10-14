# Optimización de los problemas UAFLP y FSGSP mediante algoritmo genético para el caso del sector de la confección
# de prendas de vestir de la ciudad de Cúcuta, Colombia
# Minimizar el Costo Total de Manejo de Materiales y de Penalización por Tardanza

from algGeneticoUaflp import *
from group_scheduling import *
from algGeneticoSched import *
import pandas as pd
from copy import deepcopy
# import shutil
# import pickle

# Datos de entrada para UAFLP:

datos_uaflp = pd.read_excel("Input_layout_propuesto.xlsx")
cols_uaflp = datos_uaflp.columns.values

# Departamentos (n)
departamentos = np.array(datos_uaflp["Dept"])

# Áreas de los departamentos (a_i)
areas_deptos = np.array(datos_uaflp["Area"])

# Flujos de materiales (f_ij)
flujos_mat = np.array(datos_uaflp[cols_uaflp[1:12]])

# Dimensiones de la instalación ([L_x, L_y])
dimensiones_inst = list(datos_uaflp["Facility"].dropna())

# Nombres de los departamentos
nombres_depts = list(datos_uaflp["Departamentos"].dropna())

# Datos de entrada para FSGSP:

datos_fsgsp = pd.read_excel("Input_sched_propuesto.xlsx")
cols_fsgsp = datos_fsgsp.columns.values

# Datos para la celda de manufactura 1 (CM1):

# Número de grupos (g)
grupos_cm1 = list(datos_fsgsp["G_CM1"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm1 = []
trab_cont = 1
for gr in grupos_cm1:
    n_trab = int(datos_fsgsp["J_CM1"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm1.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm1 = list(range(1, 4 + 1))

# Número de trabajos (N)
num_trabajos_cm1 = trabajos_grupos_cm1[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm1 = list(datos_fsgsp["J_CM1"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[1:5]].dropna()
t_procesamiento_cm1 = []
for ind in t_proc.index:
    t_procesamiento_cm1.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[33:37]].dropna()
t_prep_maq = []
t_preparacion_cm1 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm1:
    t_preparacion_cm1.append(t_prep_maq)

# Tiempos de entrega de los trabajos (e_j)
t_entrega_cm1 = list(datos_fsgsp["E1"].dropna())

# Costos de penalización por tardanza (w_j)
c_penalizacion_cm1 = [2.5] * num_trabajos_cm1

# Datos para la celda de manufactura 2 (CM2):

# Número de grupos (g)
grupos_cm2 = list(datos_fsgsp["G_CM2"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm2 = []
trab_cont = 1
for gr in grupos_cm2:
    n_trab = int(datos_fsgsp["J_CM2"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm2.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm2 = list(range(1, 9 + 1))

# Número de trabajos (N)
num_trabajos_cm2 = trabajos_grupos_cm2[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm2 = list(datos_fsgsp["J_CM2"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[6:15]].dropna()
t_procesamiento_cm2 = []
for ind in t_proc.index:
    t_procesamiento_cm2.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[38:41]].dropna()
t_prep_maq = []
t_preparacion_cm2 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm2:
    t_preparacion_cm2.append(t_prep_maq)

# Tiempos de entrega de los trabajos (e_j)
t_entrega_cm2 = list(datos_fsgsp["E2"].dropna())

# Costos de penalización por tardanza (w_j)
c_penalizacion_cm2 = [2.5] * num_trabajos_cm2

# Datos para la celda de manufactura 3 (CM3):

# Número de grupos (g)
grupos_cm3 = list(datos_fsgsp["G_CM3"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm3 = []
trab_cont = 1
for gr in grupos_cm3:
    n_trab = int(datos_fsgsp["J_CM3"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm3.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm3 = list(range(1, 4 + 1))

# Número de trabajos (N)
num_trabajos_cm3 = trabajos_grupos_cm3[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm3 = list(datos_fsgsp["J_CM3"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[16:20]].dropna()
t_procesamiento_cm3 = []
for ind in t_proc.index:
    t_procesamiento_cm3.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[42:]].dropna()
t_prep_maq = []
t_preparacion_cm3 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm3:
    t_preparacion_cm3.append(t_prep_maq)

# Tiempos de entrega de los trabajos (e_j)
t_entrega_cm3 = list(datos_fsgsp["E3"].dropna())

# Costos de penalización por tardanza (w_j)
c_penalizacion_cm3 = [2.5] * num_trabajos_cm3

# Creación de las clases layout y group_scheduling para los problemas del caso

# Clase Layout para el problema UAFLP
layout = Layout(num_depts=len(departamentos), areas_depts=areas_deptos,
                lados_instal=dimensiones_inst, rel_aspecto_max=4,
                flujos_materiales=flujos_mat, nom_depts=nombres_depts)

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 1
sched_cm1 = GroupScheduling(grupos=grupos_cm1, maquinas=maquinas_cm1,
                            num_trabajos=num_trabajos_cm1,
                            trabajos_grupos=trabajos_grupos_cm1,
                            num_trab_grupo=num_trabajos_k_cm1,
                            t_procesamiento=t_procesamiento_cm1,
                            t_preparacion=t_preparacion_cm1,
                            costos_tardanza=c_penalizacion_cm1,
                            fechas_entrega=t_entrega_cm1,
                            objetivo="twt")

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 2
sched_cm2 = GroupScheduling(grupos=grupos_cm2, maquinas=maquinas_cm2,
                            num_trabajos=num_trabajos_cm2,
                            trabajos_grupos=trabajos_grupos_cm2,
                            num_trab_grupo=num_trabajos_k_cm2,
                            t_procesamiento=t_procesamiento_cm2,
                            t_preparacion=t_preparacion_cm2,
                            costos_tardanza=c_penalizacion_cm2,
                            fechas_entrega=t_entrega_cm2,
                            objetivo="twt")

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 3
sched_cm3 = GroupScheduling(grupos=grupos_cm3, maquinas=maquinas_cm3,
                            num_trabajos=num_trabajos_cm3,
                            trabajos_grupos=trabajos_grupos_cm3,
                            num_trab_grupo=num_trabajos_k_cm3,
                            t_procesamiento=t_procesamiento_cm3,
                            t_preparacion=t_preparacion_cm3,
                            costos_tardanza=c_penalizacion_cm3,
                            fechas_entrega=t_entrega_cm3,
                            objetivo="twt")

# Definición de la clase Algoritmo Genético para los problemas UAFLP y FSGSP

# Algoritmo genético para el UAFLP (conjunto de parámetros 4)
ga_uaflp = AlgGeneticoLayout(tam_poblacion=100, num_generaciones=200, tam_torneo=2,
                             prob_cruce=0.9, prob_mutacion=0.1)

# Algoritmo genético para el FSGSP (conjunto de parámetros 3)
ga_fsgsp = AlgGeneticoSched(tam_poblacion=100, num_generaciones=300, tam_torneo=2,
                            prob_cruce=0.9, prob_mutacion=0.1)

# Optimización de UAFLP y FSGSP para el caso de estudio mediante GA:

n_iteraciones = 1

layout_sol = []
cm1_sched_sol = []
cm2_sched_sol = []
cm3_sched_sol = []

mhc_min = [0] * ga_uaflp.num_generaciones
twt_cm1_min = [0] * ga_fsgsp.num_generaciones
twt_cm2_min = [0] * ga_fsgsp.num_generaciones
twt_cm3_min = [0] * ga_fsgsp.num_generaciones

costo_total_iter = []
mhc = []
twt = []

iteracion = 0
while iteracion < n_iteraciones:

    # Optimización del layout de planta para el caso de estudio

    # Iniciación de la población y arreglos necesarios
    poblacion_lay = ga_uaflp.poblacion_inicial(layout)
    best_lay, best_ind_lay = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el UAFLP
    while gen < ga_uaflp.num_generaciones:

        for t in range(int(ga_uaflp.tam_poblacion / 2)):
            # Selección
            padres_lay = ga_uaflp.seleccion(layout, poblacion_lay)
            parents_lay = deepcopy(padres_lay)

            # Cruce
            children_lay = ga_uaflp.cruce(layout, parents_lay)

            # Mutación
            children_lay = ga_uaflp.mutacion(layout, children_lay)

            # Sustitución
            poblacion_lay = ga_uaflp.sustitucion(layout, poblacion_lay, children_lay)

        # Mejor fitness e individuo
        best_lay, best_ind_lay = ga_uaflp.obtener_mejor(layout, poblacion_lay)
        print("Layout:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardando solo mejor array
        # array_path = '/content/mejor_iteracion_{}.npy'.format(iteracion)
        # np.save(array_path, best_ind_lay)
        # shutil.copy(array_path, "/content/drive/My Drive")

        # Guardando con mejor
        # copy = best_ind_lay
        # copyList = list(copy)
        # copyList.append(best_lay)
        # picklePath = '/content/mejor_iteracion_{}.pickle'.format(iteracion)
        # with open(picklePath, 'wb') as f:
        #     pickle.dump(copyList, f)
        # shutil.copy(picklePath, "/content/drive/My Drive")

        # Guardar mejores y el promedio de la generación
        if mhc_min[gen] == 0 or mhc_min[gen] < best_lay:
            mhc_min[gen] = best_lay

        gen += 1

    # Guardar solución y resultados del GA para el UAFLP
    layout_sol.append(best_ind_lay)
    mhc.append(best_lay)

    # Optimización de la secuenciación para las celdas de manufactura del caso de estudio

    # Celda de manufactura 1 (CM1)
    poblacion_cm1 = ga_fsgsp.poblacion_inicial(sched_cm1)
    best_cm1, best_ind_cm1 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM1
    while gen < ga_fsgsp.num_generaciones:

        for q in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm1 = ga_fsgsp.seleccion(sched_cm1, poblacion_cm1)
            parents_cm1 = deepcopy(padres_cm1)

            # Cruce
            children_cm1 = ga_fsgsp.cruce(parents_cm1)

            # Mutación
            children_cm1 = ga_fsgsp.mutacion(children_cm1)

            # Sustitución
            poblacion_cm1 = ga_fsgsp.sustitucion(sched_cm1, poblacion_cm1, children_cm1)

        # Mejor FO e individuo
        best_cm1, best_ind_cm1 = ga_fsgsp.obtener_mejor(sched_cm1, poblacion_cm1)
        print("Group Scheduling - CM1:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if twt_cm1_min[gen] == 0 or best_cm1 < twt_cm1_min[gen]:
            twt_cm1_min[gen] = best_cm1

        gen += 1

    # Guardar solución y resultados del GA para la CM1
    cm1_sched_sol.append(best_ind_cm1)

    # Celda de manufactura 2 (CM2)
    poblacion_cm2 = ga_fsgsp.poblacion_inicial(sched_cm2)
    best_cm2, best_ind_cm2 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM2
    while gen < ga_fsgsp.num_generaciones:

        for k in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm2 = ga_fsgsp.seleccion(sched_cm2, poblacion_cm2)
            parents_cm2 = deepcopy(padres_cm2)

            # Cruce
            children_cm2 = ga_fsgsp.cruce(parents_cm2)

            # Mutación
            children_cm2 = ga_fsgsp.mutacion(children_cm2)

            # Sustitución
            poblacion_cm2 = ga_fsgsp.sustitucion(sched_cm2, poblacion_cm2, children_cm2)

        # Mejor FO e individuo
        best_cm2, best_ind_cm2 = ga_fsgsp.obtener_mejor(sched_cm2, poblacion_cm2)
        print("Group Scheduling - CM2:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if twt_cm2_min[gen] == 0 or best_cm2 < twt_cm2_min[gen]:
            twt_cm2_min[gen] = best_cm2

        gen += 1

    # Guardar solución y resultados del GA para la CM2
    cm2_sched_sol.append(best_ind_cm2)

    # Celda de manufactura 3 (CM3)
    poblacion_cm3 = ga_fsgsp.poblacion_inicial(sched_cm3)
    best_cm3, best_ind_cm3 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM3
    while gen < ga_fsgsp.num_generaciones:

        for s in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm3 = ga_fsgsp.seleccion(sched_cm3, poblacion_cm3)
            parents_cm3 = deepcopy(padres_cm3)

            # Cruce
            children_cm3 = ga_fsgsp.cruce(parents_cm3)

            # Mutación
            children_cm3 = ga_fsgsp.mutacion(children_cm3)

            # Sustitución
            poblacion_cm3 = ga_fsgsp.sustitucion(sched_cm3, poblacion_cm3, children_cm3)

        # Mejor FO e individuo
        best_cm3, best_ind_cm3 = ga_fsgsp.obtener_mejor(sched_cm3, poblacion_cm3)
        print("Group Scheduling - CM3:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if twt_cm3_min[gen] == 0 or best_cm3 < twt_cm3_min[gen]:
            twt_cm3_min[gen] = best_cm3

        gen += 1

    # Guardar solución y resultados del GA para la CM3
    cm3_sched_sol.append(best_ind_cm3)

    # Obtener costo total de alternativa para la iteración
    twt.append(best_cm1 + best_cm2 + best_cm3)
    costo_total = best_lay + best_cm1 + best_cm2 + best_cm3
    costo_total_iter.append(costo_total)

    iteracion += 1

# Guardar resultados en DataFrame con pandas

df = pd.DataFrame([mhc_min, twt_cm1_min, twt_cm2_min, twt_cm3_min, costo_total_iter,
                   mhc, twt])

df.to_excel("results_conf.xlsx")

df2 = pd.DataFrame([layout_sol, cm1_sched_sol, cm2_sched_sol, cm3_sched_sol])

df2.to_excel("results_conf_sols.xlsx")

print("Costo total de la alternativa para el caso de estudio: {}\n"
      "Costo de manejo de materiales para el mejor layout: {}\n"
      "Costo de penalización por tardanza celda de manufactura 1: {}\n"
      "Costo de penalización por tardanza celda de manufactura 2: {}\n"
      "Costo de penalización por tardanza celda de manufactura 3: {}".format(min(costo_total_iter),
                                                                             min(mhc_min),
                                                                             min(twt_cm1_min),
                                                                             min(twt_cm2_min),
                                                                             min(twt_cm3_min)))
