from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler    
import os, sys
import pandas as pd
from sklearn.svm import SVC

root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
if len(sys.argv) > 1:
    root = os.path.join(root, sys.argv[1])
files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".tsv")]

def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    #print(big_data_df.shape)
    #print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df   

def SVM_FOR_DAYS():
    data = read_all_tsvs()
    X = data.loc[:, data.columns != 1]
    y = data.iloc[:, 0]
    print(X)
    print(y)
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(X, y)
    acc = clf.score(X, y)
    print(acc)

SVM_FOR_DAYS()