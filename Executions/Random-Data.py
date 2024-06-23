import os 
import sys 
import torch
import matplotlib.pyplot as plt
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname (current)
sys.path.append(parent)

from Smoothness_Index import Kalhor_SmoothnessIndex

smi_list = []

for i in range(1000):
    size = (300, 1)


    l1 = torch.randn(size)
    l2 = torch.randn(size)

    smi_kalhor = Kalhor_SmoothnessIndex(l1
                                        ,l2,
                                        inp_normalize=True, target_normalize=True)
    
    smi_list.append(float(smi_kalhor.smi_exp(0.8)))


smi_np = np.array(smi_list)
print("average of random SMI is: ", smi_np.mean())
print("variance of random SMI is: ", smi_np.var())

plt.hist(smi_list)
plt.show()