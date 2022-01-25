
from dis import dis
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import *
from scipy.spatial.ckdtree import *
from matplotlib.collections import LineCollection
import time
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

def plot_points(coord_list,indices, path):
    fig, ax = plt.subplots()
    
    
    segs = np.zeros((len(indices),100,2))
    i = 0
    col = []
    lw = []
    for a,b in indices:
        x_0, y_0 = coord_list[a][1],coord_list[a][0]  # Coordinats for point a
        x_1, y_1 = coord_list[b][1],coord_list[b][0]  # Coordinats for point b
        x = np.linspace(x_0,x_1,100) # Create points between the points
        y = np.linspace(y_0,y_1,100)

        segs[i, :, 0] = x   # Add the 'lines' to a line matrix with segments for each connection
        segs[i, :, 1] = y
        if a in path and b in path:
            col.append('blue')
            lw.append(1)
        else:
            col.append('grey')
            lw.append(.09)
        i += 1
    
    lineseg = LineCollection(segs, linewidths = lw, color = col)
    ax.add_collection(lineseg)

    for coord in coord_list:
        coor = np.flip(coord) # Flip the matrix to make sure x is x and y is y so the map i correct
        ax.scatter(*coor, s=5, color='red')
   
    ax.autoscale()
    plt.show()
   
def construct_graph_connections(coord_list, radius):
    points = []
    dist = []
    
    for n in range(len(coord_list)):
        for m in range(n,len(coord_list)):
            avst = np.linalg.norm(coord_list[n] - coord_list[m])   # Distance between two points
            if avst <= radius:
                dist.append(avst)
                points.append(np.array([int(n), int(m)]))


    return np.array(dist), np.array(points)

def construct_fast_graph_connections(coord_list, radius):
    tree = cKDTree(coord_list)
    points = []
    dist = []
    con = []
    i = 0
    for coord in coord_list:
        points.append(tree.query_ball_point(coord,r=radius))
    
    
    for i in range(len(points)):
        for el in points[i]:
            con.append(np.array([i,el]))


        
    i = 0
    for n in points:
        for nei in n:
            dist.append(np.linalg.norm(coord_list[i] - coord_list[nei]))
        i +=1

    return np.array(con, dtype='object'), np.array(dist, dtype='object')

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

    FILENAME = 'SampleCoordinates.txt'
    if FILENAME == 'SampleCoordinates.txt':
        RADIUS = 0.08
        START_NODE = 0
        END_NODE = 5
    elif FILENAME == 'HungaryCities.txt':
        RADIUS = 0.005
        START_NODE = 311
        END_NODE = 702
    elif FILENAME == 'GermanyCities.txt':
        RADIUS = 0.0025
        START_NODE = 1573
        END_NODE = 10584



    start = time.time()
    coordinates = read_coordinate_file(FILENAME)
    end = time.time()
    func1 = end-start
    print(f'Time to read and convert coordinates: {func1:3.5f} seconds.')

    start = time.time()
    dist, connections = construct_graph_connections(coordinates, RADIUS)
    print(len(dist))
    end = time.time()
    func2 = end-start
    print(f'Time to construct graph connections: {func2:3.5f} seconds.')

    start = time.time()
    connections, dist = construct_fast_graph_connections(coordinates, RADIUS)
    print(len(dist))
    end = time.time()
    func22 = end-start
    print(f'Time to construct fast graph connections: {func22:3.5f} seconds.')


    start = time.time()
    graph = construct_graph(connections, dist)
    end = time.time()
    func3 = end-start   
    print(f'Time to construct graph: {func3:3.5f} seconds.')

    start = time.time()
    path, dist = find_shortest_path(graph,START_NODE,END_NODE)
    end = time.time()
    func4 = end-start   
    print(f'Time to find shortest path: {func4:3.5f} seconds.')

    start = time.time()
    plot_points(coordinates, connections, path)
    end = time.time()
    func5 = end-start   
    print(f'Time to plot: {func5:3.5f} seconds.')