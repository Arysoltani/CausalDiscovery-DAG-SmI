
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.cluster import KMeans
import graphviz as gviz
import matplotlib.pyplot as plt
import sys
import torch
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname (current)
sys.path.append(parent)


from Smoothness_Index import Kalhor_SmoothnessIndex
from SMI_Graph import SMI_Graph

# from Smoothness-Index.Smoothness_Index import Kalhor_SmoothnessIndex

DATASET_PATH = "../Datasets/pythetrad-simulated/"

for i in range(100):


    df = pd.read_csv(f"{DATASET_PATH}/mydata{i}.csv")
    df = df.astype({col: "float64" for col in df.columns})

    adj = pd.read_csv(f"{DATASET_PATH}/mygraph{i}.csv", header=None)

    adjacency_matrix = adj.to_numpy()
    adj_with_names = adjacency_matrix
    name_rows = adjacency_matrix[0, :]
    adjacency_matrix = np.delete(adjacency_matrix, 0, axis=0)
    adjacency_matrix = np.array(adjacency_matrix, dtype="int64")

    method = {}
    method['name'] = "Exp"
    method['gamma'] = 0.8
    print(f"************************** Test number {i} *************************")
    print(f"Number of Variables is {len(name_rows)}")
    smi_graph = SMI_Graph(adj_with_names, df, method)
    smi_graph.calculate_smi_matrix()
    # smi_graph.check_direction_of_edges()
    print("Gamma = 0.8, SMI average for directed edges is :", smi_graph.get_average_smi_edges())
    print("Gamma = 0.8, SMI average when there no edges is: ", smi_graph.get_average_smi_no_edges())

    method = {}
    method['name'] = "Exp"
    method['gamma'] = 0.4

    smi_graph = SMI_Graph(adj_with_names, df, method)
    smi_graph.calculate_smi_matrix()
    # smi_graph.check_direction_of_edges()
    print("Gamma = 0.4, SMI average for directed edges is :", smi_graph.get_average_smi_edges())
    print("Gamma = 0.4, SMI average when there no edges is: ", smi_graph.get_average_smi_no_edges())
    
    method = {}
    method['name'] = "Linear"
    smi_graph = SMI_Graph(adj_with_names, df, method)
    smi_graph.calculate_smi_matrix()
    print("Linear, SMI average for directed edges is :", smi_graph.get_average_smi_edges())
    print("Linear, SMI average when there no edges is: ", smi_graph.get_average_smi_no_edges())
    # print(smi_graph.find_graph_knowing_num_edges(200))
