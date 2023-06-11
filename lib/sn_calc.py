import numpy as np
import pandas as pd
from numpy import log as ln
from numpy import nan
import math


def larger(values):
    """Calculates the larger-the-best S/N from a list of values"""
    # total = 0
    # print(values)
    all_ones = all(value == 1 for value in values)
    all_zeros=all(value==0 for value in values)
    if all_ones or all_zeros:
        # print(values)
        return nan
    
    # for value in values:
    #     total += 1 / (value ** 2)
    
    # return -10*ln(abs(total / len(values)),math.e)
    total = np.sum(1 / (values ** 2))
    if len(values)>0:
        return -10 * np.log(np.abs(total / len(values)))
    else:
        # print(values)
        return 0

def smaller(values):
    """Calculates the smaller-the-best S/N from a list of values"""
    # total1 = 0
    # for value in values:
    #     total1 += value ** 2
    
    # -10*ln(abs(total / len(values)),math.e)
    total = np.sum(values ** 2)
    # print(total1, total)
    if len(values)==0:
        return 0
    else:
        return -10 * np.log(np.abs(total / len(values)))

def nominal(values):
    """Calculates Nominal the best based on a list of values"""
    # return -10*ln(np.std(values**2),math.e)
    # try:
    all_zeros=all(value==0 for value in values)
    if all_zeros:
        # print(values)
        return nan
    else:
        return -10 * np.log(np.std(values ** 2))
    # except RuntimeWarning:
    #     print(values)
    #     return 0