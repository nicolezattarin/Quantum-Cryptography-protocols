import numpy as np
import pandas as pd
from scipy.io import loadmat 

def df_from_mat(path):
    """
    Load the data from the .mat file and return a dataframe.
    time is expressed in seconds
    """
    print('Loading data: ', path)
    mat = loadmat(path)
    time = mat['data'][0][0][0][0]*1e-12
    mintime = min(time)
    newtime = [t-mintime for t in time]
    channel = mat['data'][0][0][1][0]
    df = pd.DataFrame(channel)
    df['time'] = newtime
    df.columns=[ 'channel','time']
    return df

def find_coincidences (df):
    """
    Read the dataset and keep only the events which have a coincidence 
    between channel 2 with channel 3 or channel 4. You can decide 
    the coincidence window, a suggested value is around 3 ns.
    """
    print('Finding coincidences...')
    ch3 = df[df['channel']!=4]
    ch4 = df[df['channel']!=3]
    ch3 = ch3.diff()
    ch4 = ch4.diff()
    ch3['channel']=3
    ch4['channel']=4
    ch3 = ch3[ch3['channel']!=0]
    ch4 = ch4[ch4['channel']!=0]
    coincidences = ch3.append(ch4)
    return coincidences

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", default='data/d_state_measured_on_da_basis.mat', help="filename.", type=str)

def main(filename):
    """
    Read the data from the .mat file given as argument and find the coincidences.
    coincidences are saved in a .txt file in the coincidences folder.
    """
    import os
    df = df_from_mat(filename)
    if (os.path.isdir('coincidences')==False):
        os.mkdir('coincidences')
    coincidences = find_coincidences(df)
    coincidences.to_csv('coincidences/'+filename[5:-4]+'_coincidences.txt')
    
if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)

    