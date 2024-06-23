import numpy as np



def add_data(arr_inp, ind):
    file_out = open(f"./data{ind}.csv", "w")
    for i in range(len(arr_inp)):
        if(i != 0):
            file_out.write(",")
        file_out.write(f"X{i}")
    file_out.write("\n")
    for i in range(len(arr_inp[0])):
        for j in range(len(arr_inp)):
            if(j != 0):
                file_out.write(",")
            file_out.write(str(arr_inp[j][i]))
        file_out.write("\n")
    
def add_graph(graph_inp, sz, ind):
    file_out = open(f"./graph{ind}.csv", "w")
    for i in range(sz):
        if(i != 0):
            file_out.write(",")
        file_out.write(f"X{i}")
    file_out.write("\n")
    for i in range(sz):
        for j in range(sz):
            if(j != 0):
                file_out.write(",")
            if((i, j) in graph_inp and (j, i) in graph_inp):
                file_out.write("1")
            elif((i, j) in graph_inp):
                file_out.write("2")
            elif((j, i) in graph_inp):
                file_out.write("3")
            else:
                file_out.write("0")
        file_out.write("\n")
#######################Graph1#################################
############ n = 5 ##############

l = [0 for i in range(5)]

l[0] = np.random.normal(size = 300)
l[2] = np.cos(l[0] * 2)
l[4] = np.sin(l[2]) 
l[3] = np.sin(l[4] ** 2)
l[1] = np.cos(np.sin(np.exp(l[3])))

graph = []
graph.append((0, 2))
graph.append((2, 4))
graph.append((4, 3))
graph.append((3, 1))

add_data(l, 1)

add_graph(graph, 5, 1)