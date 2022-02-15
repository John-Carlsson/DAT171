""" Dat 171, Computer Assignment 1, written by John Carlsson, spring of 2022 """

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import *
from scipy.spatial.ckdtree import *
from matplotlib.collections import LineCollection
import time
import math


def read_coordinate_file(filename):
    """ Take input coordinates and remove unwanted characters, returns a np.array. Input should be a .txt file with each row looking like this: '{0., -1.}' 
    param filenmae: .txt file with rows like this '{0., -1.}
    type filename: string
    
    return coordinates: a list of list like this [[0. -1.], [2,3]]
    type coordinates: np.array of np.arrays of two floats 
    """
    lista = []
    not_allowed = '{}'
    r = 1

    with open(filename, 'r') as file:  # Comma separated numbers, '{a,b}'
        for line in file:
            for char in not_allowed:
                line = line.strip(char)  # Remove the brackets , unwanted blankspace and /n from the string
                line = line.strip()
            coord = line.split(',')
            coord = [(r*math.log(math.tan(math.pi/4.0 + np.radians(float(coord[0]))/2.0))), (r*math.radians(float(coord[1])))]  # transform from string to float and a,b to x,y
            # transform from string to float and a,b to x,y
            lista.append(np.array(coord))

    return np.array(lista)  # Create  an array of arrays with coordinates

def plot_points(coord_list, indices, path):
    """ Function for plotting the map and the shortest path between two points
    param coord_list: list of list of coordinates
    type coord_list: np.array of np.arrays of two floats

    param indices: a list of lists with cities that connect
    type indices: np.array of np.array of two integers

    param path: A list of the shortest path of visited nodes from a to b
    type path: list


    
    
    

    return: plots a graph
    
    """
    plt.gca().set_aspect('equal')
    ax = plt.subplot(1,1,1)    
    segs = np.empty((len(indices), 2, 2))  # Create the empty array to allocate the linesegment, the dimensions are known
    col = ['grey'] * len(indices)  # Define color and linewidth for the most common type of line
    lw = [.3] * len(indices)
    

    # [coord_list[path]]
    # segs = coord_list[indices]
    for i, c in enumerate(indices):  # Add the 'lines' to a line matrix with segments for each connection
        segs[i, :, 0] = [coord_list[c[0]][1], coord_list[c[1]][1]]   # Cordinates for the two points
        segs[i, :, 1] = [coord_list[c[0]][0], coord_list[c[1]][0]]   # Cordinates for the two points
        if c[0] in path and c[1] in path:
            col[i] = 'blue'
            lw[i] = 1

    
    
    
    # Add lines to plot
    lineseg = LineCollection(segs, linewidths = lw, color = col)
    ax.add_collection(lineseg)

    # Add scatter
    coord_list = np.flip(coord_list)
    ax.scatter(coord_list[:,0],coord_list[:,1], s=5, color='red')
    
    plt.show()
   
def construct_graph_connections(coord_list, radius):
    """ Setup the graph connections within a given radius
        param coord_list: np.array of np.array of floats like this [[x1,y1], [x2,y2]]
        type coord_list: np.array of np.array of two floats

        param radius: a radius
        type coord_list: int

        
        return con: a list of indices which are within the given radius
        type con: np.array of np arrays of two ints

        return distance: the distance between the points
        type distance: np.array of floats
    """
    con = []
    distance = []

    for n, a in enumerate(coord_list):
        for m in range(n+1, len(coord_list)):                         # Makes the graph 'undirected' to avoid redundancy
            dist = np.linalg.norm(a - coord_list[m])                  # Distance between two points
            if dist <= radius:
                distance.append(dist)
                con.append([n, m])

    return np.array(distance), np.array(con)

def construct_fast_graph_connections(coord_list, radius):
    """ Setup the graph connections within a given radius

    param coord_list: np.array of np.array of floats like this [[x1,y1], [x2,y2]]
    type coord_list: np.array of np.array of two floats

    param radius: a radius
    type coord_list: int
    
    return con: a list of indices which are within the given radius
    type con: np.array of np arrays of two ints

    return distance: the distance between the points
    type distance: np.array of floats
    """
    tree = cKDTree(coord_list)
    distance = []
    con = []
    points = (tree.query_ball_point(coord_list, r=radius))   #  Make an adjacency list where the first index is node and the second
                                                             #  is a list with neighbours within range

    for i, point in enumerate(points):
        for el in point:
            if el >= i:                                      #  Make a list of connections, since the graph is "undirected" there will
                con.append(np.array([i, el]))                          #  only be one "road" between nodes since you can go both ways on the same road

    con_array = np.array(con)
    conec = np.array([coord_list[con_array[:,0]], [coord_list[con_array[:,1]]]])
    distance = np.linalg.norm((conec[0]) - (conec[1]), axis=-1)
    
    return con_array, distance[0]

def construct_graph(indices, distance, N):
    """ Construct the graph with indices and the distance between them 
    param indices: list of indices
    param distance: distance between indices
    param N: The sixe of the matrix, also the length of the distance list
    type indices: np.array
    type distance: np.array
    type N: int

    return: a sparse matrix where the indexes are the cities and the values at their location is the distance between them
    type value: csr_matrix
    """
    
    indices = indices.T
    sparse = csr_matrix((distance, indices),shape=(N,N))

    return sparse

def find_shortest_path(graph, start_node, end_node):
    """ Uses a graph, a start and an end node to find the shortest path using the csgraph.shortest path function 

    param graph: a graph
    param start_node: start node
    param end node: end node

    type graph: csr_matrix
    type start_node: int
    type end_node: int

    return path: a list of visited nodes from start to end node,
    return dist: total distance of the path
    type path: list
    type dist: float
    
    
    """

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
    N = len(dist)
    
    graph = construct_graph(connections, dist, N)
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

