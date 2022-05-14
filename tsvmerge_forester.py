from audioop import avg
from cgitb import handler
import pandas as pd
import os, sys
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score

#from MakeGraph import read_all_tsvs

root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
if len(sys.argv) > 1:
    root = os.path.join(root, sys.argv[1])
files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".tsv")]

path_to_drop_tsv = os.path.join(os.path.dirname(__file__),"logs", "split")
print(path_to_drop_tsv)
def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    #print(big_data_df.shape)
    #print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df

class Tsv_handler:

    def Run_Forrest_Run():
        data = read_all_tsvs()
        X = data.loc[:, data.columns != 1]
        y = data.iloc[:, 0]
        print(X)
        print(y)
        avg_acc =0
        avg_recall=0
        avg_precision=0
        x = 0
        for x in range(9):
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
            #print(avg_acc)
            avg_recall += recall_score(y_test, prediction_of_y)
            avg_precision += precision_score(y_test, prediction_of_y)
            #print(recall)
            #print(precision)
            x+=1
            print(x)
        
        print(avg_acc/9)
        print(avg_recall/9)
        print(avg_precision/9)
        return avg_acc/9





    if __name__ == "__main__":
        #fname = "aoutsub48"
        #data_to_split = read_all_tsvs()
        #train_data = data_to_split.sample(frac=0.7)
        #test_data = data_to_split.drop(train_data.index)
        #train_data.to_csv(os.path.join(path_to_drop_tsv, f"{fname}_TRAIN.tsv"),sep="\t", header=None, index=False)
        #test_data.to_csv(os.path.join(path_to_drop_tsv, f"{fname}_TEST.tsv"),sep="\t", header=None, index=False)
        Run_Forrest_Run()
    

    
