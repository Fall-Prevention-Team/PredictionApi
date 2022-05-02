import pandas as pd
import os, sys
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split


files = [os.path.join('.', f) for f in os.listdir('.') if f.endswith(".tsv")]


def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    print('Concatted shape:',big_data_df.shape)
    #print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df

def Run_Forrest_Run(data, r=10):
    X = data.loc[:, data.columns != 1]
    y = data.iloc[:, 0]
    #print(X)
    #print(y)
    
    avg_acc = 0
    for x in range(1,r+1):
        x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.25)
        feat_clf = SelectFromModel(RandomForestClassifier(n_estimators=100))
        clf = RandomForestClassifier(n_estimators=100)
        clf.fit(x_train, y_train)
        feat_clf.fit(x_train, y_train)
        #features_selected = x_train.columns[(feat_clf.get_support())]
        #print(len(features_selected))
        #print(features_selected)
        #print(clf.estimators_[0])
        prediction_of_y = clf.predict(x_test)
        avg_acc += accuracy_score(y_true=y_test, y_pred=prediction_of_y)
        print(f'{x:2}','~',avg_acc/x, '%')

    print('Final:',avg_acc/r*100)
    return avg_acc/r


d = read_all_tsvs()
Run_Forrest_Run(d)
