import inout
from sys import argv
import random

if argv[1] == 'small':
    entrada = [0, 0, 0, 0, 9, 11, 12, 18, 18, 25]
    salida = [4, 6, 8, 12, 15, 20, 25, 29, 33, 40]
    inout.inout_flow(entrada, salida, maxflow=True)

elif argv[1] == 'large' and argv[2] is not None:
    # Try with random numbers
    entrada = []
    for i in range(int(argv[2])):
        inter_arrival = random.randint(0, 10)
        if i == 0:
            entrada.append(inter_arrival)
            pass
        entrada.append(entrada[-1] + inter_arrival)

    # Primera unidad saliente
    salida = [entrada[0] + random.randint(5, 10)]
    for i in range(1, len(entrada)):
        flow_time = random.randint(5, 20)
        salida.append(max(entrada[i], salida[i - 1]) + flow_time)

    inout.inout_flow(entrada, salida, grid=True, maxflow=True)
