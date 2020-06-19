#%% [markdown]
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
sData = pd.read_csv('E:/Documents/UNE/HUMS_301/sectionDataSet.csv', header=0)

# Random Seed Number
seed = 7

# Data Set 1
sColumns = ['Phrases', 'Measures', 'Notes', 'Duration', 'Syllables']
pColumns = ['Measures', 'Notes', 'Duration', 'Syllables']

sX = sData[sColumns] # feature matrix
sy = sData['Section'] # labels vector
pX = pData[pColumns] # feature matrix
py = pData['Phrase'] # labels vector

# Data Set 2
sCol2 = ['Section','Phrases', 'Measures', 'Notes', 'Duration', 'Syllables']
pCol2 = ['Phrase', 'Measures', 'Notes', 'Duration', 'Syllables']

sX2 = sData[sCol2] # feature matrix
sy2 = sData['Frottala'] # labels vector
pX2 = pData[pCol2] # feature matrix
py2 = pData['Frottala'] # labels vector

def ScatterAllFeatures():
    selected_columns = sColumns + ['Section']
    sb.pairplot(sData[selected_columns], hue='Section', plot_kws={'alpha': 0.3})

    selected_columns = pColumns + ['Phrase']
    sb.pairplot(pData[selected_columns], hue='Phrase', plot_kws={'alpha': 0.3})

    selected_columns = sCol2 + ['Frottala']
    sb.pairplot(sData[selected_columns], hue='Frottala', plot_kws={'alpha': 0.3})

    selected_columns = pCol2 + ['Frottala']
    sb.pairplot(pData[selected_columns], hue='Frottala', plot_kws={'alpha': 0.3})

def ViolinAllFeatures():
    selected_columns = sColumns + ['Section']
    plt.figure(figsize=(20, 20))
    for column_index, column in enumerate(selected_columns):
        if column == 'Section':
            continue
        plt.subplot(3, 4, column_index + 1)
        sb.violinplot(x = 'Section', y = column, data = sData[selected_columns])

    selected_columns = pColumns + ['Phrase']
    plt.figure(figsize=(30, 20))
    for column_index, column in enumerate(selected_columns):
        if column == 'Phrase':
            continue
        plt.subplot(3, 4, column_index + 1)
        sb.violinplot(x = 'Phrase', y = column, data = pData[selected_columns])

def PearsonCorrelation():
    plt.figure(figsize = (20, 16))
    sCor = sData.corr()
    sb.heatmap(sCor, annot = True, cmap = plt.cm.Reds)
    plt.show()

    plt.figure(figsize = (20, 16))
    pCor = sData.corr()
    sb.heatmap(pCor, annot = True, cmap = plt.cm.Red)
    plt.show()

def Section_DecTreeClassify():
    model_accuracies = []
    # Split the dataset into 80% training, 20% testing and test 1,000 times
    for i in range(1000):
        sX_train, sX_test, sy_train, sy_test = train_test_split(sX, sy, train_size=0.8, random_state = i)

        decision_tree_classifier = DecisionTreeClassifier(random_state = seed)
        decision_tree_classifier.fit(sX_train, sy_train)
        classifier_accuracy = decision_tree_classifier.score(sX_test, sy_test)
        model_accuracies.append(classifier_accuracy)

    sb.distplot(model_accuracies)

def Phrase_DecTreeClassify():
    model_accuracies = []
    # Split the dataset into 80% training, 20% testing and test 1,000 times
    for i in range(1000):
        pX_train, pX_test, py_train, py_test = train_test_split(pX, py, train_size=0.8, random_state = i)

        decision_tree_classifier = DecisionTreeClassifier(random_state = seed)
        decision_tree_classifier.fit(pX_train, py_train)
        classifier_accuracy = decision_tree_classifier.score(pX_test, py_test)
        model_accuracies.append(classifier_accuracy)
        
    sb.distplot(model_accuracies)

def SectionLearningCurve():
    decision_tree_classifier = DecisionTreeClassifier(random_state = seed)
    sX_train, sX_test, sy_train, sy_test = train_test_split(sX, sy, train_size=0.8, random_state = seed)
    pX_train, pX_test, py_train, py_test = train_test_split(pX, py, train_size=0.8, random_state = seed)
    
    # Activate to generate SECTION learning curve scores
    train_sizes, train_scores, val_scores = learning_curve(estimator = decision_tree_classifier, X = sX_train, y = sy_train, train_sizes = np.linspace(0.1, 1.0, 20), cv = 10, n_jobs = 1)
    # Activate to generate PHRASE learning curve scores
    # train_sizes, train_scores, val_scores = learning_curve(estimator = decision_tree_classifier, X = pX_train, y = py_train, train_sizes = np.linspace(0.1,1.0,20),cv=10,n_jobs=1)

    # Calculate the result averages and standard deviation
    train_mean = np.mean(train_scores, axis = 1)
    train_std = np.std(train_scores, axis = 1)
    val_mean = np.mean(val_scores, axis = 1)
    val_std = np.std(val_scores, axis = 1)

    # Plot the training learning curve
    plt.plot(train_sizes, train_mean, color='green', marker='o', markersize=5, label='training accuracy')
    plt.fill_between(train_sizes, train_mean + train_std, train_mean - train_std, alpha=0.15, color='green')

    # Plot the validation learning curve
    plt.plot(train_sizes, val_mean, color='blue', linestyle='--', marker='s', markersize=5, label='validation accuracy')
    plt.fill_between(train_sizes, val_mean + val_std, val_mean - val_std, alpha=0.15, color='blue')

    # Plot settings
    plt.xlabel('Number of training samples')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.ylim([0.8, 1])
    plt.tight_layout()

    plt.show()

ScatterAllFeatures()
# ViolinAllFeatures()
# PearsonCorrelation()
# Section_DecTreeClassify()
# Phrase_DecTreeClassify()
# SectionLearningCurve()
# print('pX: %s, %s' % (type(pX), pX.shape))
# print('py: %s, %s' % (type(py), py.shape))

print('Finished!')
# %%
