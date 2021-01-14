import matplotlib.pyplot as plt
from algorithms import search as b_search
from algorithms import dynamic_count as d_count


def inout_flow(inflow, outflow, grid=False, maxflow=False):
    """Toma como input 2 secuencias con tiempos inflow y outflow (en formato numérico o datetime).
    Plotea un gráfico con los inflow y outflow acumulados, además del nivel WIP, desde el inicio
    del proceso (t=0) hasta la salida de la última unidad WIP."""

    if not len(inflow) == len(outflow):
        return "Error: inflow y outflow no tienen la misma extensión"
    units_length = len(inflow)

    plt.figure(figsize=(15, 8))

    # Obtener número acumulado de unidades entrantes/salientes y max flow time (mft)
    units = []
    mft = 0
    for i in range(units_length):
        # Esto sirve para graficar la forma 'pre' del step plot (inflow)
        units.append(i)
        # Esto sirve para hallar los tiempos máximos de flujo
        mft = max(mft, outflow[i] - inflow[i])

    # Cumulative Inflow
    # El último 'inflow time' debe coincidir con el último 'outflow time' (salida de todos los WIP)
    proper_in_units = units + [units[-1] + 1]
    proper_inflow = inflow + [outflow[-1]]
    plt.step(proper_inflow, proper_in_units, where='pre', label="inflow", color='k', linewidth=2.5)

    # Cumulative Outflow (en t=0 han salido 0 unidades)
    post_units = [x+1 for x in units]
    proper_out_units = [0] + post_units
    proper_outflow = [0] + outflow
    plt.step(proper_outflow, proper_out_units, where='post', label="outflow", color='g')

    # Work in Progress (WIP)
    # Puntos de flujo (inflow u outflow)
    flow_points = list(set(proper_inflow + proper_outflow))
    flow_points.sort()

    # Nivel en el 1er flow_point
    first_point = flow_points[0]
    level_in = 0
    for point in proper_inflow:
        if point == first_point:
            level_in += 1
        else:
            break
    level_out = 0
    point_units_in = [level_in]
    point_units_out = [level_out]

    # WIP: Diferencia de niveles en el punto inicial
    wip = [point_units_in[0] - point_units_out[0]]

    # Niveles del 2do al último flow_point
    for i in range(1, len(flow_points)):

        # Si el point está solo en proper_inflow
        if b_search(proper_inflow, flow_points[i]) and not b_search(proper_outflow, flow_points[i]):
            level_in += d_count(flow_points[i], proper_inflow, level_in)
            point_units_in.append(level_in)
            point_units_out.append(point_units_out[-1])

        # Si el point está solo en proper_outflow
        elif b_search(proper_outflow, flow_points[i]) and not b_search(proper_inflow, flow_points[i]):
            level_out += 1
            point_units_out.append(level_out)
            point_units_in.append(level_in)

        # Si está en ambos
        else:
            level_in += d_count(flow_points[i], proper_inflow, level_in)
            level_out += 1
            point_units_in.append(level_in)
            point_units_out.append(level_out)

        # WIP: Diferencia de niveles restantes
        wip.append(point_units_in[i] - point_units_out[i])

    # Plotear WIP
    plt.fill_between(flow_points, wip, step="post", alpha=0.25, color="k")

    # Plot largest waiting time as a double-arrow line: <--------------------->
    if maxflow:
        units_with_mft = []

        # Obtener índices de todas las unidades con el flow time máximo
        for i in range(units_length):
            if outflow[i] - inflow[i] == mft:
                units_with_mft.append(i)

        # Plotear flechas doble
        for i in units_with_mft:
            plt.annotate(text=f'{outflow[i] - inflow[i]}', color="r", fontsize=13,
                         xy=(inflow[i], i + 0.5), xytext=(outflow[i], i + 0.5),
                         arrowprops=dict(arrowstyle="<|-|>", mutation_scale=25,
                                         color="r", linestyle='-'),
                         verticalalignment='center',
                         )
    # # Ajustar eje X
    # axes = plt.gca()
    # axes.set_xlim([1606468521.0,1606476181.0])

    if grid:
        plt.grid()
    plt.legend()
    plt.show()
