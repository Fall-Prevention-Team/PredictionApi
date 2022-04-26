import os, sys
import pandas as pd
import numpy as np
root = os.path.join(os.path.dirname(__file__), "logs", "tsvs")
files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".tsv")]

def read_all_tsvs():
    list_of_df =[pd.read_csv(o, sep="\t", header=None) for o in files]
    big_data_df = pd.concat(list_of_df, axis=0, ignore_index=True)
    print(big_data_df.shape)
    print(big_data_df)
    df = big_data_df.iloc[: , 1:]
    return df

mdf = read_all_tsvs()
if '-s' in sys.argv:
    fname = f'single_l-{len(mdf)}'
    mdf.to_csv(f"{root}/../split/{fname}.tsv",sep="\t", header=None, index=False)
else:
    for i, col in enumerate(mdf):
        if not i % 5 == 0: 
            mdf.pop(col)
    msk = np.random.rand(len(mdf)) < 0.8
    train = mdf[msk]
    test = mdf[~msk]
    fname = f'all-{str(mdf.shape).replace(", ", "-")}'
    train.to_csv(f"{root}/../split/{fname}_TRAIN.tsv",sep="\t", header=None, index=False)
    train.to_csv(f"{root}/../split/{fname}_TEST.tsv",sep="\t", header=None, index=False)
