from asyncore import read
from cProfile import label
import os
import matplotlib.pyplot as plt
import pandas as pd

root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
files = [os.path.join(root, f) for f in os.listdir(root) if f.__contains__("SLX1")]

def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    print(big_data_df.shape)
    print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df

def GraphFromTSV():
        data_frame = read_all_tsvs()
        #plt.subplot(3,1,1)
        x_values = data_frame.iloc[:, 1::3]
        y_values = data_frame.iloc[:, 2::3]
        z_values = data_frame.iloc[:, 3::3]
        all_rows=8;
        for index in range(len(data_frame)):
            x = x_values.loc[index]
            y = y_values.loc[index]
            z = z_values.loc[index]
            plt.plot(x, label="X label")
            plt.plot(y, label="Y label")
            plt.plot(z, label="Z label")
            plt.title("Fall number: " + str(index+1))
            plt.xlabel("number of datapoint")
            plt.ylabel("value detoned")
            plt.legend()
            plt.show()

            
        #plt.subplot(3,1,2)

        #plt.subplot(3,1,3)
        #plt.tight_layout()
       # path = self.root_path_to_img + folderpath + ".png"
       # plt.savefig(path)
        #plt.cla()
        #plt.clf()
        print(x_values)
        return None

GraphFromTSV()