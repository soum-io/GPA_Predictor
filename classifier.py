'''
By: Michael Shea

This python script uses the filitered data to to train and test a model to use
for the prediction.
'''

import numpy as np
from numpy import array
from sklearn import preprocessing, model_selection, linear_model, svm
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# create dataframe of the cleaned data created in data_cleanup.py
# I use one_hot_encoding to encode the courses and teachers into numerical
# values.
df = pd.read_csv('filteredComplete.csv').sort_values("year")
one_hot_course = pd.get_dummies(df['course'])
df = df.drop('course', axis=1)
df = df.join(one_hot_course)

one_hot_teacher = pd.get_dummies(df['teacher'])
df = df.drop('teacher', axis=1)
df = df.join(one_hot_teacher)

# save the one hot encoded dataframe to a csv in case it needs to be used again.
df.to_csv('filteredCompleteOHE.csv', sep=',',index = False)

# create training and testing data
df = pd.read_csv('filteredCompleteOHE.csv')
X = np.array(df.drop(['gpa'],1))
X = preprocessing.scale(X)
Y = np.array(df[['gpa']])
cutoff = 37000  #number of values in training data
# the training data will be the first number of datapoints up to the cutoff n
# number, the testing will be the rest. 
X_train = X[:cutoff,:]
Y_train = Y[:cutoff,:]
X_test = X[cutoff:, :]
Y_test = Y[cutoff:, :]

print( Y.reshape(Y.size).shape)

# declare what model to use
clf = svm.SVR(kernel = "linear").fit(X_train, Y_train.reshape(Y_train.size))

# save model as a pickle file for later use
with open('BayesianRidgeFull.pickle', 'wb') as f:
    pickle.dump(clf,f)
    
pickle_in = open('BayesianRidgeFull.pickle', 'rb')
clf = pickle.load(pickle_in)

#print out the accuracy of the model on the testing data
accuracy = clf.score(X_test, Y_test.reshape(Y_test.size))
print(accuracy)









