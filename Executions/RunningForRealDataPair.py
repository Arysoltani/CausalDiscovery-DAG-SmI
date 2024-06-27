import numpy as np
import os
import sys
import torch
import matplotlib.pyplot as plt
import scipy.stats as stats


FOLDER_PATH = "../Datasets/RealWorldPairs/"

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname (current)
sys.path.append(parent)


from Smoothness_Index import Kalhor_SmoothnessIndex
from SMI_Graph import SMI_Graph

cnt1 = 0
cnt2 = 0
smi_real = np.array([])
smi_rand = np.array([])

for i in range(1, 41):

    if(i < 10):
        data = np.loadtxt(f"{FOLDER_PATH}pair000{i}.txt", delimiter=" ")
    elif(i < 100):
        with open(f"{FOLDER_PATH}pair00{i}.txt", "r+") as f:  # Open in read-write mode
            data = f.read().replace("\t", " ")
            f.seek(0)  # Move the file pointer to the beginning
            f.truncate()  # Truncate the file content
            f.write(data)     
            f.close()   
            data = np.loadtxt(f"{FOLDER_PATH}pair00{i}.txt", delimiter=" ")
    else:
        data = np.loadtxt(f"{FOLDER_PATH}pair0{i}.txt", delimiter=" ")
    col1 = data[:, 0]
    col2 = data[:, 1]



    col1_rand = torch.randn((len(col1), 1))
    col2_rand = torch.randn((len(col2), 1))

    col1 = torch.from_numpy(np.array(col1).reshape(len(col1), 1))
    col2 = torch.from_numpy(np.array(col2).reshape(len(col2), 1))
 
    correlation, p_value = stats.pearsonr(col1.flatten(), col2.flatten())
    correlation_rand, p_value = stats.pearsonr(col1_rand.flatten(), col2_rand.flatten())


    smi_kalhor_cause = Kalhor_SmoothnessIndex(col1, 
                                        col2, 
                                        inp_normalize=True, target_normalize=True)
    smi_kalhor_effect = Kalhor_SmoothnessIndex(col2, 
                                        col1, 
                                        inp_normalize=True, target_normalize=True)
    if(smi_kalhor_cause.smi_linear().item() > smi_kalhor_effect.smi_linear().item()):
        cnt1 += 1
    else:
        cnt2 += 1

    smi_kalhor_rand = Kalhor_SmoothnessIndex(col1_rand, 
                                        col2_rand, 
                                        inp_normalize=True, target_normalize=True)
    
    smi_real = np.append(smi_real, smi_kalhor_cause.smi_linear().item())
    smi_rand = np.append(smi_rand, smi_kalhor_rand.smi_linear().item())

    print("correlation ",correlation, end = " ")
    print("correlation random",correlation_rand, end = " ")
    print("SMI in real data cause: ", smi_kalhor_cause.smi_linear().item(), end = " ")

    print("SMI in real data effect: ", smi_kalhor_effect.smi_linear().item(), end = " ")

    print("SMI in random: ", smi_kalhor_rand.smi_linear().item())

print(smi_real.var())
print(smi_rand.var())