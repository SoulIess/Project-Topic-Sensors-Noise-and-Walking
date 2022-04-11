import sys
import os
import numpy as np
import pandas as pd
from utils import *

def main():
    current = os.getcwd()
    final = os.path.join(current, r'output')
    if not os.path.exists(final):
        os.makedirs(final)
    
    #day 1 data
    paths = ['data/ankle.csv', 'data/arm.csv', 'data/pocket.csv', 'data/ankle_2.csv', 'data/arm_2.csv', 'data/pocket_2.csv']
    dfs = []

    for path in paths:
        dfs.append((setUp(path, 0.5, 0.5), path))

    for df, path in dfs:
        name = path.replace('data/', '')
        name = name.replace('.csv', '')
        outputAccelWithButter(df, name)

    ankle, _ = dfs[0]
    outputSpeed(ankle)
    
    #day 2 data
    paths = ['data/forward.csv', 'data/backward.csv', 'data/male.csv', 'data/female.csv']
    dfs = []
    for path in paths:
        dfs.append((setUp(path, 0.5, 0.5), path))
        
    for df, path in dfs:
        name = path.replace('data/', '')
        name = name.replace('.csv', '')
        outputAccelWithButter(df, name)

    forward,_ = dfs[0]
    backward,_ = dfs[1]
    outputFB(forward, backward)

    male,_ = dfs[2]
    female,_ = dfs[3]
    outputGender(male, forward, female)

if __name__ == '__main__':
    main()
