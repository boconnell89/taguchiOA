import pandas as pd
from . import sn_calc
from numpy import nan
import numpy as np

import sys

"""Calculates the level average for each level in an array, for a given response variable"""

def LAA(OA, Data, factors, Response, type):

    # print('')
    # print(Data)
    # print(analyses)
    # print(factors)
    # print(OA)
    # print(max(OA[c])+1)
    tmp=factors.copy()
    # print (tmp)
    # for Response in analyses: ######### Need to have this 
        # print(c)
    for c in list(OA.columns):
        # continue
        # print('\t', c, max(OA[c])+1)
        
        # print(Response)
        # if type in analyses[Response][analyses[Response].notnull()].values:
        #     print('\t', Response)
        # #     # factors['{} {}'.format(c, colSuffix)]=nan
            # # # print(factors)
            # print(max(OA[c]))
        for i in range(1,max(OA[c])+1):
            # sys.stdout.write('{}'.format(str( Data[OA[c] == i]['{} {}'.format(Response, type)].mean())))
            average = Data[OA[c] == i]['{} {}'.format(Response, type)].mean()
            # factors.at[i-1,'{} {}'.format(c, colSuffix)]=average
            tmp.at[i-1, c]=average
            # print(factors, i-1, c)
            # print()
    return tmp