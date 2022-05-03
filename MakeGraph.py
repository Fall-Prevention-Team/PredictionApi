from asyncore import read
from cProfile import label
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler as scale
import pandas as pd

root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
files = [os.path.join(root, f) for f in os.listdir(root) if f.__contains__("KBX1")]

def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    print(big_data_df.shape)
    print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df

def GraphFromTSV():
        data_frame = read_all_tsvs()            
        sc = scale()
        scale_dataframe = sc.fit_transform(data_frame)
        #plt.subplot(3,1,1)
        x_values = data_frame.iloc[:, 1::3]
        y_values = data_frame.iloc[:, 2::3]
        z_values = data_frame.iloc[:, 3::3]

        for index in range(len(data_frame)):
            x_scale = scale_dataframe[index][1::3]
            y_scale = scale_dataframe[index][2::3]
            z_scale = scale_dataframe[index][3::3]
            x_raw = x_values.loc[index]
            y_raw = y_values.loc[index]
            z_raw = z_values.loc[index]

            fig, (raw_plot, scale_plot) = plt.subplots(2)

            raw_plot.plot(x_raw, label="X label")
            raw_plot.plot(y_raw, label="Y label")
            raw_plot.plot(z_raw, label="Z label")
            raw_plot.set_title("raw data")  

            scale_plot.plot(x_scale, label="X label")
            scale_plot.plot(y_scale, label="Y label")
            scale_plot.plot(z_scale, label="Z label")
            scale_plot.set_title("scaled data")

            fig.suptitle("Fall number: " +str(index+1))
            raw_plot.legend()
            scale_plot.legend()
            plt.show()

        


GraphFromTSV()