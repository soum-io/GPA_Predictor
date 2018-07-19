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
from fastai.structured import *
from fastai.column_data import *
np.set_printoptions(threshold=50, edgeitems=20)


# list for categorical column titles for embeddings
cat_vars = ['course', 'teacher', 'year', 'semester', 'semesters taught']
# list for continous columns titles - empty, but may change later
contin_vars = []

# create dataframe of the cleaned data created in data_cleanup.py
# I use one_hot_encoding to encode the courses and teachers into numerical
# values.
df = pd.read_csv('filteredComplete.csv').sort_values("semester")
df = df.sort_values("year")
df_future_sem = pd.read_csv('course_teacher_full.csv')
# print(df.head(15 # print for debugging

# get the last year and semester on record, as this will be our validation set
last_year = int(df['year'].iloc[-1])
last_semester = int(df['semester'].iloc[-1])
start_index = -1
for idx in range(df.shape[0]):
    if df['year'].iloc[idx] == last_year and df['semester'].iloc[idx] == last_semester:
        start_index = idx; break
# print(last_year, " ", last_semester, " ", df.shape[0], " ", start_index) # print for debugging

# list of validation set indices
val_idx = np.array([i for i in range(start_index, df.shape[0])])

# will not actually be ordered, but embedded as will be seen down below
for v in cat_vars:
    df[v] = df[v].astype('category').cat.as_ordered()
    df_future_sem[v] = df_future_sem[v].astype('category').cat.as_ordered()


# the following code is used if continous variables will be used in the future.
# use 0 to fill na for now
for v in contin_vars:
    df[v] = df[v].fillna(0).astype('float32')
    df_future_sem[v] = df_future_sem[v].fillna(0).astype('float32')

# turn categorical columns into int representations to use embeddingsself.
# After, ensure columns are of type category
df_train, y, nas = proc_df(df, 'gpa', do_scale=False)
for v in cat_vars: df_train[v] = df_train[v].astype('category').cat.as_ordered()

df_test, _, nas = proc_df(df_future_sem, do_scale=False, na_dict = nas)
# we will use log scale for answers
yl = np.log(y)

def inv_y(a):
    return np.exp(a)

# we will use Root-mean-squared percent error as our metric
def exp_rmspe(y_pred, targ):
    targ = inv_y(targ)
    pct_var = (targ - inv_y(y_pred))/targ
    return math.sqrt((pct_var**2).mean())

# set y bounds
max_log_y = np.max(yl)
y_range = (0, max_log_y*1.2)

# path is directory where data lives - I am using the current directory
PATH = "./"

# create fastai data object
md = ColumnarModelData.from_data_frame(PATH, val_idx, df_train, yl.astype(np.float32),
    cat_flds = cat_vars, bs=128, test_df = df_test)

# get the number of unique values in each categorical columns
cat_sz = [(c, len(df_train[c].cat.categories)+1) for c in cat_vars]
# use cardinality (number of categoires) for each catigorical column to pick
# embeddigns size
emb_szs = [(c, min(50, (c+1)//2)) for _,c in cat_sz]

# obtain learning rate
m = md.get_learner(emb_szs, len(df_train.columns)-len(cat_vars),
                   0.04, 1, [1000,1000, 500], [0.001,0.01, .02], y_range=y_range)
                   # test_df = train_df.iloc[val_idx])

# this code will plot and show that the best learning rate is .01 - uncomment to verify
# m.lr_find()
# m.sched.plot(100)
# plt.show()
lr = .005

# train model
# best that I found -> m.fit(lr, 3, metrics=[exp_rmspe], cycle_len=2)
m.fit(lr, 1, metrics=[exp_rmspe], cycle_len=2)

# get validation predicitons and save them with thier true answers to a csv file
# so the results can be inspected externally
x,y_val=m.predict_with_targs()
x = x.reshape(-1); y_val = y_val.reshape(-1)
x = np.exp(x); y_val = np.exp(y_val)

with open("viz_predictions.csv", 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',',
                                quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["True", "Prediction", "Difference"])
    for i in range(x.size):
        writer.writerow([y_val[i], x[i], abs(y_val[i] - x[i])])


# make predictions on test set, and save it as a csv file
pred_test = m.predict(True)
pred_test = np.exp(pred_test)
pred_test = np.around(pred_test, decimals = 2)
df_future_sem['predicted gpa'] = pred_test
pred_year = int(df_future_sem['year'].iloc[1])
pred_semester = int(df_future_sem['semester'].iloc[1])
if(pred_semester == 1):
  pred_semester = "Spring"
elif (pred_semester == 2 ):
  pred_semester = "Summer"
else:
  pred_semester = "Fall"
csv_fn = str(pred_semester)+str(pred_year)+"Predictions.csv"
df_future_sem.to_csv(csv_fn, index = False)
