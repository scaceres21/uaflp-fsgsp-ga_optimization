# Determinación de la tardanza ponderada total para el caso de confecciones actual
# Flexible Job Shop

import pandas as pd
import numpy as np


# Datos de entrada para la situación actual:

df = pd.read_excel("Input_sched_actual.xlsx")

# Programa de producción de lotes de trabajos (shortest processing time)
schedule = list(df["Schedule"])

# Familias de los lotes de trabajo en programa
families = list(df["Families_Sched"])

# Secuencias de operación y tiempos de procesamiento en cada estación:
# 1 - Máquinas collarín, 2 - Máquinas fileteadoras, 3 - Máquinas planas
# sequences = [[secuencia operación j1], [tiempo procesamiento j1], ...]
sq = list(df["Sequence"])
sequences = []
for ind_c, col in enumerate(df.columns[3:46]):
    proc_time = list(df[col].dropna())
    if sq[ind_c] == 1:
        sequences.append([[1, 2, 1], proc_time])
    elif sq[ind_c] == 2:
        sequences.append([[3, 2, 3, 2, 3, 1, 3, 1, 3], proc_time])
    elif sq[ind_c] == 3:
        sequences.append([[1], proc_time])

# Tiempos de preparación dependiente de la secuencia de las familias de productos
# setup = [[tiempo de preparación inicial], [tiempo de preparación fam 1], ...]
setup = list(np.array(df[df.columns[47:]].dropna()))


# Estructuras de datos para acumular tiempos de terminación de trabajos

# Tiempo de terminación en cada máquina de cada estación
# Collarín: 6 máquinas, Fileteadora: 4 máquinas, Plana: 4 máquinas
# completion_prev_machines = [[tiempo terminación cada máquina estación1], ...]
completion_prev_machines = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# Familias predecesoras en cada máquina en cada estación
# fam_prev_machines = [[familia anterior en cada máquina estación 1], ...]
fam_prev_machines = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


# Inicio del programa para determinar la tardanza ponderada total

completion_jobs = []
for ind_j, j in enumerate(schedule):

    fam = families[ind_j]
    completion_prev_stage = 0
    completion = 0
    for ind_s, seq in enumerate(sequences[j - 1][0]):
        pos_min = completion_prev_machines[seq - 1].index(min(completion_prev_machines[seq - 1]))
        prev_family = fam_prev_machines[seq - 1][pos_min]
        completion = max(completion_prev_stage, completion_prev_machines[seq - 1][pos_min] +
                         setup[prev_family][fam - 1]) + sequences[j - 1][1][ind_s]

        completion_prev_stage = completion
        completion_prev_machines[seq - 1][pos_min] = completion
        fam_prev_machines[seq - 1][pos_min] = fam

    completion_jobs.append(completion)


# Calculando el makespan y la tardanza ponderada total para el caso de estudio

makespan = completion_jobs[-1]
total_completion_time = 0

tardiness_cost = 2.5
due_date = 36000
total_weighted_tardiness = 0
for c in completion_jobs:
    tardiness = max(0, c - due_date)
    total_weighted_tardiness += tardiness * tardiness_cost
    total_completion_time += c

print("El costo de tardanza total para la situación actual del caso de estudio es:\n", total_weighted_tardiness)