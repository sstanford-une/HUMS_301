#%%
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Data Options
pData = pd.read_csv('E:/Documents/UNE/HUMS_301/phraseDataSet.csv', header=0)
sData = pd.read_csv('E:/Documents/UNE/HUMS_301/sectionDataSet.csv', header=0)

# Column Options
pCol1 = ['Measures', 'Notes', 'Duration', 'Syllables']
pCol2 = ['Phrase', 'Measures', 'Notes', 'Duration', 'Syllables']
sCol1 = ['Phrases', 'Measures', 'Notes', 'Duration', 'Syllables']
sCol2 = ['Section','Phrases', 'Measures', 'Notes', 'Duration', 'Syllables']

# Target Column Options
tar1 = 'Phrase'
tar2 = 'Section'
tar3 = 'Frottala'

class DataAnalyser:
   
    def __init__(self, data, columns, target):
        self.data = data
        self.columns = columns
        self.target = target

    def AnalyseData(self):

        print(self.data.describe())

        # Variables used in function
        seed = 7
        X = self.data[function]
        y = self.data[self.target]

        # Create a PEARSONS CORRELATION chart with all features
        plt.figure(figsize = (20, 20))
        Cor = self.data.corr()
        sb.heatmap(Cor, annot = True, cmap = plt.cm.Reds)
        plt.show()

        # Create a SCATTER PLOT with all features
        selected_columns = self.columns + [self.target]
        sb.pairplot(self.data[selected_columns], hue = self.target, plot_kws={'alpha': 0.3})

        # Create VIOLIN PLOTS of all features
        selected_columns = self.columns + [self.target]
        plt.figure(figsize=(13, 13))
        for column_index, column in enumerate(selected_columns):
            if column == self.target:
                continue
            plt.subplot(3, 4, column_index + 1)
            sb.violinplot(x = self.target, y = column, data = self.data[selected_columns])
        plt.show()

        # TRAIN_TEST_SPLIT
        # Split the dataset into 80% training, 20% testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = seed)

        # Decision Tree Classifier
        decision_tree_classifier = DecisionTreeClassifier(random_state=seed)

        # Split the dataset into 80% training, 20% testing and test 1,000 times
        model_accuracies = []
        for i in range(1000):
            sX_train, sX_test, sy_train, sy_test = train_test_split(sX, sy, train_size=0.8, random_state = i)

            decision_tree_classifier = DecisionTreeClassifier(random_state = seed)
            decision_tree_classifier.fit(sX_train, sy_train)
            classifier_accuracy = decision_tree_classifier.score(sX_test, sy_test)
            model_accuracies.append(classifier_accuracy)

        sb.distplot(model_accuracies)


#phraseAnalysis = DataAnalyser(pData, pCol1, tar1)
#phraseAnalysis.AnalyseData()
print('Analysis Complete')

for i in pData.Measures:
    print(i)
#%%