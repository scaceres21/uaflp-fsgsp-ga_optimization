# Determinación del MHC, distancia total y layout para el estado actual del caso de confecciones

from algGeneticoUaflp import *
import pandas as pd

# Datos de entrada:

data = pd.read_excel("Input_layout_actual.xlsx")

# Departamentos y áreas requeridas
dpts = np.array(data["Dept"])
areas = np.array(data["Area"])
aspect_ratio = 4
dim_facility = list(data["Facility"].dropna())
material_flow = np.array(data[data.columns[1:7]])
names_depts = ["Recepción-Despacho", "Confección", "Estampado", "Terminación", "Oficina", "Almacén"]

# Crear clase Layout con las características de la instalación

confeccion_actual = Layout(num_depts=len(dpts), areas_depts=areas, lados_instal=dim_facility,
                           rel_aspecto_max=aspect_ratio, flujos_materiales=material_flow,
                           nom_depts=names_depts)

# Definir ubicación actual de los departamentos y bahías, de acuerdo con cromosoma
cromo_dep = np.array([1, 5, 4, 3, 2, 6])
cromo_bay = np.array([0, 0, 0, 1, 0, 1])

# Determinar MHC y layout para el caso actual

mhc_actual = confeccion_actual.fitness(cromo_dep, cromo_bay)

confeccion_actual.mostrar_layout(cromo_dep, cromo_bay)

print("El costo de manejo de materiales para el layout actual es:\n", round(mhc_actual, 2))