import torch 
import numpy as np
from Smoothness_Index import Kalhor_SmoothnessIndex

class SMI_Graph: 

    def __init__(self, graph_original, dataframe_input, method):
        self.graph_inp = graph_original 
        self.cols = []
        name_rows = graph_original[0, :]
        num_rows = dataframe_input.shape[0]
        self.method = method
        self.adjacency_matrix = np.delete(graph_original, 0, axis=0)
        self.adjacency_matrix = np.array(self.adjacency_matrix, dtype="int64")

        for i in range(dataframe_input.shape[1]):
            self.cols.append(torch.from_numpy(np.array(dataframe_input.loc[:, name_rows[i]]).reshape(num_rows, 1)))

    def smi_nodes(self, i, j):
        smi_kalhor = Kalhor_SmoothnessIndex(self.cols[i], 
                                            self.cols[j], 
                                            inp_normalize=True, target_normalize=True)
        if(self.method['name'] == "Linear"):
            return smi_kalhor.smi_linear()
        elif(self.method['name'] == "Exp"):
            return smi_kalhor.smi_exp(self.method['gamma'])
    
    def calculate_smi_matrix(self):
        self.smi_mat = np.zeros((len(self.cols),len(self.cols)))
        for i in range(len(self.cols)):
            for j in range(len(self.cols)):
                if(i == j):
                    continue
                smi_kalhor = Kalhor_SmoothnessIndex(self.cols[i], 
                             self.cols[j], 
                             inp_normalize=True, target_normalize=True)
                self.smi_mat[i, j] = self.smi_nodes(i, j)
    
    def get_average_smi_edges(self):
        sum_smi_edges = sum(self.smi_mat[i, j] for i in range(len(self.cols)) for j in range(len(self.cols)) if (self.adjacency_matrix[i, j] == 2 or self.adjacency_matrix[i, j] == 1)
                                                                                                                 and i != j)
        return sum_smi_edges / ((self.adjacency_matrix == 2).sum() + (self.adjacency_matrix == 1).sum())

    def get_average_smi_no_edges(self):
        sum_smi_edges = sum(self.smi_mat[i, j] for i in range(len(self.cols)) for j in range(len(self.cols)) if (self.adjacency_matrix[i, j] != 2 and self.adjacency_matrix[i, j] != 1) 
                            and i != j)
        mat_non_edge = self.adjacency_matrix != 2
        mat_non_edge &= self.adjacency_matrix != 1
        np.fill_diagonal(mat_non_edge, 0)
        return sum_smi_edges / mat_non_edge.sum()

    def find_graph_knowing_num_edges(self, num_edges):
        arg_pred_edges = self.smi_mat.flatten().argsort()[-num_edges:]
        arg_pred_edges = np.unravel_index(arg_pred_edges, self.smi_mat.shape)
        print(self.adjacency_matrix[arg_pred_edges])
        print(self.smi_mat[arg_pred_edges])
        print(self.smi_mat[self.adjacency_matrix == 2])

        self.graph_edges_pred = np.zeros_like(self.smi_mat)
        self.graph_edges_pred[arg_pred_edges] = 1
        condition = (self.graph_edges_pred == 1) & (self.adjacency_matrix == 1) | (self.graph_edges_pred == 1) & (self.adjacency_matrix == 2)
        return(np.sum(condition))
    
    def check_direction_of_edges(self):
        correct = 0
        incorrect = 0
        sum1 = 0
        sum2 = 0
        for i in range(self.adjacency_matrix.shape[0]):
            for j in range(self.adjacency_matrix.shape[0]):
                if(self.adjacency_matrix[i, j] == 2):
                    print(self.smi_mat[i, j], self.smi_mat[j, i])
                    if(self.smi_mat[i, j] > self.smi_mat[j, i]):
                        sum1 += self.smi_mat[i, j]
                        correct += 1
                    else:
                        sum2 += self.smi_mat[i, j]
                        incorrect += 1
        print(correct)
        print(sum1 / correct)
        print(incorrect)
        print(sum2 / incorrect)

    def print_edges(self):
        for i in range(self.adjacency_matrix.shape[0]):
            for j in range(self.adjacency_matrix.shape[0]):
                if(self.adjacency_matrix[i, j] == 2):
                    print(i, j)

    def print_matrix(self):
        for i in range(self.adjacency_matrix.shape[0]):
            for j in range(self.adjacency_matrix.shape[0]):
                if(j != 0):
                    print(",", end = '')
                print(self.smi_mat[i, j], end = '')
            print()
    
    