from cgi import test
from tkinter.messagebox import NO
from numpy import inner
import pandas as pd
import os

root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".tsv")]


def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    print(big_data_df.shape)
    print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df


from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
def Run_Forrest_Run():
    data = read_all_tsvs()
    X = data.loc[:, data.columns != 1]
    y = data.iloc[:, 0]
    print(X)
    print(y)
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.1)
    feat_clf = SelectFromModel(RandomForestClassifier(n_estimators=20))
    clf = RandomForestClassifier(n_estimators=20)
    clf.fit(x_train, y_train)
    feat_clf.fit(x_train, y_train)
    features_selected = x_train.columns[(feat_clf.get_support())]
    print(len(features_selected))
    print(features_selected)
    print(clf.estimators_[0])
    prediction_of_y = clf.predict(x_test)
    acc = accuracy_score(y_true=y_test, y_pred=prediction_of_y)
    print(acc)
    return acc




#Run_Forrest_Run()

if __name__ == "__main__":
    data_to_split = read_all_tsvs()
    train_data = data_to_split.sample(frac=0.5)
    test_data = data_to_split.drop(train_data.index)
    train_data.to_csv("./aout_TRAIN.tsv",sep="\t", header=None, index=False)
    test_data.to_csv("./aout_TEST.tsv",sep="\t", header=None, index=False)
    

    