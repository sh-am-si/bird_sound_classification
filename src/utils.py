import json
import os
import re
import pandas as pd
import numpy as np

from pymongo import MongoClient

path_info = os.path.join('./data', 'info')
path_sound = os.path.join('./data', 'sound_db')
path_spect = os.path.join('./data', 'pics_db')

def generate_df(threshold=100, size_limit=16_000_000):
    """[summary]

    Args:
        threshold (int, optional): minimal number of records. Defaults to 100.
            threshold==100 -> 2 namse
            threshold==20 -> 119 names
         size_limit (int, optional): max size of audio file. Defaults to 16_000_000.

    Returns:
        [type]: [description]
    """

    bddf = pd.read_json(open(os.path.join('./data', 'info.json')), orient='index')
    dfa = bddf[bddf['class']=='A']

    mfdf = dfa['name'].value_counts()
    mfdf20 = mfdf[mfdf > threshold]

    ndf = dfa[dfa['name'].isin(mfdf20.index)]

    ndf.reset_index(inplace=True)
    ndf.rename(columns={'index': 'key'}, inplace=True)

    ndf['size'] = [os.stat(os.path.join(path_sound, f"sound_{k}.mp3")).st_size for k in ndf['key']]
    nndf = ndf[ndf['size'] < size_limit]

    return nndf

def get_mongo_access():
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["birdDB"]
    mycol = mydb["birdSoundDB"]

    return mycol

def get_mp3_fname(ind):
    fname = os.path.join(path_sound, f'sound_{ind}.mp3')
    assert os.path.isfile(fname), f'{fname} does not exist'
    return fname

def get_spectrum_fname(ind):
    fname = os.path.join(path_spect, f'spectrum_{ind}.png')
    assert os.path.isfile(fname), f'{fname} does not exist'
    return fname