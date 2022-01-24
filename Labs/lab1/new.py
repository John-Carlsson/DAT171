""" Första inlämningsuppgiften i DAT 171"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix as csmat
from matplotlib.collections import LineCollection as linecol

def read_coordinate_file(filename):
    lista = []
    not_allowed = '{}'
    r = 1
    pi = np.pi
    ln = np.log
    tan = np.tan
    with open(filename, 'r') as file:  # Comma separated numbers, {a,b}
        line = file.readline()
        while line:
            for char in not_allowed:

                line = line.replace(char, '').strip()  # Remove the brackets and /n from the string
            coord = line.split(',')
            coord = [float(coord[0])*pi*r/180, r*ln(tan(pi/4 + pi*float(coord[1])/360))]  # transform from string to float and ma,b to xy

            lista.append(np.array(coord))
            line = file.readline()

    return np.array(lista)  # Create  an array of arrays with coordinates

def plot_points(coord_list,indices):

    indices = indices.T.reshape(-1,1,2)

    indices = [x for x in indices]

    print(indices)
    fig, ax = plt.subplots()


    for coordinate in coord_list:
        ax.scatter(*coordinate)
    linecolors = linecol(indices)
    ax.add_collection(linecolors)

    plt.show()

def construct_graph_connections(coord_list, radius):
    points = []
    dist = []
    for n in range(len(coord_list)):
        for m in range(len(coord_list)):
            avst = np.linalg.norm(coord_list[n] - coord_list[m])   # Distance between two points
            if avst <= radius:
                dist.append(avst)
                points.append(np.array([int(n), int(m)]))


    return np.array(dist), np.array(points)

def construct_graph(indices, distance):
    indices = indices.T
    sparse = csmat((distance, indices))

    return sparse

if __name__ == '__main__':

    FILENAME = 'SampleCoordinates.txt'
    data = read_coordinate_file(FILENAME)

    dist, points = construct_graph_connections(data, 0.08)
    sparse = construct_graph(points, dist)
    plot_points(data, points)
