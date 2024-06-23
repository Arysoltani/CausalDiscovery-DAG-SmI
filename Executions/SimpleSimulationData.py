import os 
import sys 
import torch
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


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
plt.xlabel("SMI")
plt.ylabel("Count")
plt.title("SMI histogram")

average_smi = smi_np.mean()
variance_smi = smi_np.var()

x_norm = np.linspace(average_smi - 3*np.sqrt(variance_smi), average_smi + 3*np.sqrt(variance_smi), 100)

# Calculate probability density function (PDF) of the normal distribution
pdf_norm = stats.norm.pdf(x_norm, average_smi, np.sqrt(variance_smi)) * 10  # Using standard deviation

# Add normal distribution to the plot
plt.plot(x_norm, pdf_norm, label="Normal Distribution", color='red')

# Customize the plot
plt.legend()
plt.grid(True)

plt.show()