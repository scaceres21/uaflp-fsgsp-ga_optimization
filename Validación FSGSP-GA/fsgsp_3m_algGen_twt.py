# The flowshop group scheduling problem (Salmasi et al, 2010 (2-machine))

from group_scheduling import *
from algGeneticoSched import *
import numpy as np
from copy import deepcopy
import pandas as pd


results = []
reps = 0
while reps < 6:

    opt_ga = []

    # Datos de entrada

    # number of groups -> [1, 2]
    groups = list(range(1, np.random.randint(2, 5 + 1, 1)[0] + 1))

    # set of jobs belonging to group k (G_k) -> [[1, 2], [3, 4, 5]]
    jobs_groups = []
    job_cont = 1
    for gr in groups:
        n_jobs = np.random.randint(5, 7 + 1, 1)[0]
        jobs = list(range(job_cont, job_cont + n_jobs))
        jobs_groups.append(jobs)
        job_cont += n_jobs

    # number of machines (m)
    machines = [1, 2, 3]

    # Number of jobs (n_o) -> 5
    num_jobs = jobs_groups[-1][-1]

    # number of jobs in group k (n_k) -> [2, 3]
    num_jobs_k = []
    for gr in jobs_groups:
        num_jobs_k.append(len(gr))

    # run time of job j on machine i (p_ji) -> run_time[job-1][machine-1]
    run_time = []
    for job in range(num_jobs):
        job_list = []
        for mach in machines:
            job_list.append(np.random.randint(1, 20, 1)[0])
        run_time.append(job_list)

    # run_time Structure:
    # [# M1  M2
    # [# 16,  7], #j1
    # [#  5, 15]] #jn...

    # setup time of group k processed after group t on machine i (a_tki) -> 2-machines
    # setup_time[machine-1][previous group][next group-1]
    setup_time = []
    for mac in machines:
        mach_list = []
        for gro in range(len(groups) + 1):
            group_list = []
            for g in groups:
                if gro == g:
                    group_list.append(0)
                else:
                    if mac == 1:
                        group_list.append(np.random.randint(1, 50 + 1, 1)[0])
                    elif mac == 2:
                        group_list.append(np.random.randint(17, 67 + 1, 1)[0])
                    elif mac == 3:
                        group_list.append(np.random.randint(45, 95 + 1, 1)[0])
            mach_list.append(group_list)
        setup_time.append(mach_list)

    # setup_time structure:
    # [# Machine 1
    # [# G1  G2 --> Next group
    # [# 35, 10],  # G0 - Reference group --> Previous group
    # [# 22, 19]], # G1 ...
    # [# Machine 2
    # [# 25, 40],  # G0
    # [# 18, 39]]] # G1...

    # large positive number (M)
    M = 999999

    # tardiness penalties -> [3, 4, 5, 2, 1] - Keshavarz et al (2019): DU[1, 5]
    weight_tard = np.random.randint(1, 5 + 1, num_jobs)

    # Crear clase GroupScheduling para la instancia del problema:

    group_sched = GroupScheduling(grupos=groups, maquinas=machines, num_trabajos=num_jobs,
                                  trabajos_grupos=jobs_groups, num_trab_grupo=num_jobs_k,
                                  t_procesamiento=run_time, t_preparacion=setup_time,
                                  costos_tardanza=weight_tard, objetivo="twt")

    # Determinar las fechas de entrega de los trabajos -> [123, 204, 155, 108, 103]

    # Obtener makespan óptimo para definir fechas de entrega de la instancia - Keshavarz et al (2019)
    makespan = group_sched.optimizar_milp(objetivo="makespan")

    # Fechas de entrega "relajadas" -> loose: DU[0.3 * C_max, 1.7 * C_max]
    due_date = np.random.randint(0.3 * makespan, 1.7 * makespan, num_jobs)
    # Fechas de entrega "estrictas" -> tight: DU[0.1 * C_max, 0.9 * C_max]
    # due_date = np.random.randint(0.1 * makespan, 0.9 * makespan, num_jobs)
    group_sched.fechas_entrega = due_date

    # Obtener valor óptimo para la instancia del FSGSP
    # TCT
    # optimo = group_sched.optimizar_milp(objetivo="tct")
    # TWT
    optimo = group_sched.optimizar_milp_twt()

    opt_ga.append(optimo)

    # Crear clase algGeneticoSched con los parámetros del algoritmo genético

    ga_sched = AlgGeneticoSched(tam_poblacion=200, num_generaciones=400, tam_torneo=3,
                                prob_cruce=0.8, prob_mutacion=0.2)

    poblacion = ga_sched.poblacion_inicial(group_sched)
    best, best_individual = ga_sched.obtener_mejor(group_sched, poblacion)

    fit_gen = []
    individuos_min = []
    generaciones = 0

    while generaciones < ga_sched.num_generaciones:

        for t in range(int(ga_sched.tam_poblacion/2)):

            # Seleccionar los individuos padre para cruce mediante torneo
            padres = ga_sched.seleccion(group_sched, poblacion)
            parents = deepcopy(padres)

            # Cruzar los dos individuos seleccionados mediante PMX
            children = ga_sched.cruce(parents)

            # Mutar los individuos hijos
            children = ga_sched.mutacion(children)

            # Sustituir los nuevos individuos por los peores individuos de la población
            poblacion = ga_sched.sustitucion(group_sched, poblacion, children)

        print(poblacion)

        # Obtener mejor fitness y mejor individuo de la generación
        best, best_individual = ga_sched.obtener_mejor(group_sched, poblacion)

        # Guardar mejor fitness y mejor individuo
        fit_gen.append(best)
        individuos_min.append(best_individual)
        print("Generación n°: ", generaciones)
        print("Rep: ", reps)

        if best == optimo:
            break

        # Pasar a la siguiente generación
        generaciones += 1

    opt_ga.append(min(fit_gen))
    opt_ga.append(round((opt_ga[1] - opt_ga[0])/opt_ga[0], 3))
    results.append(opt_ga)

    reps += 1

df = pd.DataFrame(results)
df.to_excel("results_fsgsp_twt.xlsx")
