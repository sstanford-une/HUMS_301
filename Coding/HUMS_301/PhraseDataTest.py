#%%[markdown]
import os
import numpy as np
import pandas as pd
import sklearn.datasets as datasets 
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import seaborn as sb

pData = pd.read_csv('E:/Documents/UNE/HUMS_301/phraseDataSet.csv', header=0)

seed = 7

pCol1 = ['Measures', 'Notes', 'Duration', 'Syllables']
pCol2 = ['Phrase', 'Measures', 'Notes', 'Duration', 'Syllables']

pX = pData[pCol1] # feature matrix
py = pData['Phrase'] # labels vector
pX2 = pData[pCol2] # feature matrix
py2 = pData['Frottala'] # labels vector

selected_columns = pCol2 + ['Frottala']
sb.pairplot(pData[selected_columns], hue ='Frottala', plot_kws={'alpha': 0.3})

# PearsonCorrelation():
plt.figure(figsize = (20, 20))
pCor = pData.corr()
sb.heatmap(pCor, annot = True, cmap = plt.cm.Reds)
plt.show()

# %%
