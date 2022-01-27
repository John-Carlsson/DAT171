
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import *
from scipy.spatial.ckdtree import *
from matplotlib.collections import LineCollection
import time
import math


def read_coordinate_file(filename):
    lista = []
    not_allowed = '{}'
    r = 1

    with open(filename, 'r') as file:  # Comma separated numbers, '{a,b}'
        line = file.readline()
        while line:
            for char in not_allowed:
                line = line.replace(char, '').strip()  # Remove the brackets , unwanted blankspace and /n from the string
            coord = line.split(',')
            coord = [(r*math.radians(float(coord[1]))), (r*math.log(math.tan(math.pi/4.0 + np.radians(float(coord[0]))/2.0)))]  # transform from string to float and a,b to x,y
            coord.reverse()
            # transform from string to float and a,b to x,y
            lista.append(np.array(coord))
            line = file.readline()

    return np.array(lista)  # Create  an array of arrays with coordinates


def plot_points(coord_list, indices, path):
    fig, ax = plt.subplots()    
    segs = np.empty((len(indices), 2, 2))  # Create the empty array to allocate the linesegment, the dimensions are known
    col = ['grey'] * len(indices)  # Define color and linewidth for the most common type of line
    lw = [.3] * len(indices)
    start = time.time()

    for i, c in enumerate(indices):  # Add the 'lines' to a line matrix with segments for each connection
        segs[i, :, 0] = [coord_list[c[0]][1], coord_list[c[1]][1]]   # Cordinates for the two points
        segs[i, :, 1] = [coord_list[c[0]][0], coord_list[c[1]][0]]   # Cordinates for the two points
        if c[0] in path and c[1] in path:
            col[i] = ('blue')
            lw[i] = (1)
    end = time.time()
    print('time to draw lines:', end-start)
    
    # Add lines to plot
    lineseg = LineCollection(segs, linewidths = lw, color = col)
    ax.add_collection(lineseg)

    # Add scatter
    start = time.time()
    coord_list = np.flip(coord_list)
    ax.scatter(coord_list[:,0],coord_list[:,1], s=5, color='red')
    end = time.time()
    print('time to scatter:', end-start)
    ax.autoscale()
    plt.show()

   
def construct_graph_connections(coord_list, radius):
    con = []
    distance = []
    
    for n in range(len(coord_list)):
        for m in range(n, len(coord_list)):                         # Makes the graph 'undirected' to avoid redundancy
            dist = np.linalg.norm(coord_list[n] - coord_list[m])   # Distance between two points
            if dist <= radius:
                distance.append(dist)
                con.append(np.array([int(n), int(m)]))

    return np.array(distance), np.array(con)


def construct_fast_graph_connections(coord_list, radius):
    tree = cKDTree(coord_list)
    points = []
    distance = []
    con = []
    for coord in coord_list:
        points.append(tree.query_ball_point(coord,r=radius))  #  Make an adjacency list where the first indax is node and the second
                                                              #  is a list with neighbours within range
   
    for i in range(len(points)): 
        for el in points[i]:
            if el >= i:                                       #  Make a list of connections, since the graph is "undirected" there will
                con.append(np.array([int(i), int(el)]))       #  only one "road" between nodes since you can go both ways on the same road

    for i, nei in con:
        distance.append(np.linalg.norm(coord_list[i] - coord_list[nei]))  # Calculate distance between nodes within range
        

    return np.array(con), np.array(distance)


def construct_graph(indices, distance):
    indices = indices.T
    sparse = csr_matrix((distance, indices))

    return sparse


def find_shortest_path(graph, start_node, end_node):
    cs, pred = csgraph.shortest_path(graph, indices=start_node, directed = False, return_predecessors=True)
    dist = cs[end_node]
    path = []
    current = end_node
    while current != -9999:
        path.append(current)
        current = pred[current]
    path.reverse()
    return path, dist


if __name__ == '__main__':

    """ Settings: """
    SCENARIO = '3'  # '1' ,'2' or '3' for sample, hungary or germany respectively
    SPEED = 'fast'  # can be 'slow' or 'fast'

    if SCENARIO == '1':
        FILENAME = 'SampleCoordinates.txt'
        RADIUS = 0.08
        START_NODE = 0
        END_NODE = 5
    elif SCENARIO == '2':
        FILENAME = 'HungaryCities.txt'
        RADIUS = 0.005
        START_NODE = 311
        END_NODE = 702
    elif SCENARIO == '3':
        FILENAME = 'GermanyCities.txt'
        RADIUS = 0.0025
        START_NODE = 1573
        END_NODE = 10584

    """ Read coordinates """
    print(f'Filnamn: {FILENAME}')
    start = time.time()
    coordinates = read_coordinate_file(FILENAME)
    end = time.time()
    func1 = end-start
    print(f'Time to read and convert coordinates: {func1:3.5f} seconds.')

    """ Graph connections """
    if SPEED.lower() == 'slow':
        """ Graph connections slow """
        start = time.time()
        dist, connections = construct_graph_connections(coordinates, RADIUS)
        end = time.time()
        func2 = end-start
        func22 = 0
        print(f'Time to construct graph connections: {func2:3.5f} seconds.')

    elif SPEED.lower() == 'fast':
        """ Faster graph connections """
        start = time.time()
        connections, dist = construct_fast_graph_connections(coordinates, RADIUS)
        end = time.time()
        func22 = end-start
        func2 = 0
        print(f'Time to construct fast graph connections: {func22:3.5f} seconds.')

    """ Construct graph """
    start = time.time()
    graph = construct_graph(connections, dist)
    end = time.time()
    func3 = end-start   
    print(f'Time to construct graph: {func3:3.5f} seconds.')

    """ Shortest path """
    start = time.time()
    path, dist = find_shortest_path(graph, START_NODE, END_NODE)
    end = time.time()
    func4 = end-start   
    print(f'Time to find shortest path: {func4:3.5f} seconds.')
    print(f'The shortest path from {START_NODE} to {END_NODE} is:\n {path}')
    print(f'The total distance is {dist:3.5f}')

    """ Plot """
    func5 = func1+func2+func22+func3+func4
    print(f'Time to run program excluding plotting: {func5:3.5f} seconds.')
    plot_points(coordinates, connections, path)


    