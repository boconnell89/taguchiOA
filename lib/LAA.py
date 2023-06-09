import pandas as pd
from . import sn_calc
from numpy import nan

"""Calculates the level average for each level in an array, for a given response variable"""

def LAA(OA, Data, setup, analyses, colSuffix):
    for c in list(OA.columns):
        for Response in analyses:
            # setup['{} {}'.format(c, colSuffix)]=nan
            for i in range(1,max(OA[c])+1):
                # print( Data[OA[c] == i])
                average = Data[OA[c] == i]['{} {}'.format(Response, colSuffix)].mean()
                # setup.at[i-1,'{} {}'.format(c, colSuffix)]=average
                setup.at[i-1, c]=average
    return setup
    