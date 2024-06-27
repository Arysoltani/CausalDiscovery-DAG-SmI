import pandas as pd
import sys 
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname (current)
sys.path.append(parent)

from Smoothness_Index import Kalhor_SmoothnessIndex
from SMI_Graph import SMI_Graph


def print_matrix_to_file(matrix, filename, df):

  with open(filename, "w") as f:
    f.write(" ".join(list(df.columns)) + "\n")
    for row in matrix:
      row_string = " ".join(map(str, row)) + "\n"  
      f.write(row_string)

dataset_path = input()
method_type = input()
if(method_type == "Exp"):
    gama_input = input()

delimiter = ","
if(dataset_path[-3:-1] == "tx"):
   delimiter = "\t"

df = pd.read_csv(dataset_path, delimiter = delimiter)
df = df.astype({col: "float64" for col in df.columns})

method = {}
method['name'] = method_type
if(method_type == "Exp"):
    method['gamma'] = gama_input


smi_graph = SMI_Graph([], df, method, False)
smi_mat = smi_graph.calculate_smi_matrix()
file_out = input("Output is ready please enter file name to write: ")
print_matrix_to_file(smi_mat, file_out, df)