import numpy as np
import pandas as pd
import math
import lib
import sys
import os

class taguchiOA:
    def __init__(self, OA, experiment=''):
        self.OA = lib.parseOA.parse(OA)
        self.data=lib.parseExperiment.parseExperiment(experiment)
        # Create a list of common column names between OA and Setup
        for i, column in enumerate(self.data['Factors'].columns):
            self.OA.rename(columns={i: column}, inplace=True)
        

    def calc_values(self, suffix):
        """Calculates the Level Average, and S/N indicated in data["Data"]. Suffix= Mean, LTB, STB, or NTB"""
        self.data[suffix]=(lib.LAA.LAA(self.OA, self.data['Data'], self.data['Factors'], self.data['Setup'].columns, suffix))
        # print(self.data['LAA'])
    
    def merge_replicates(self):
        """merges replicates. """
        for column in self.data['Setup'].columns: #Get different basic response variables
            if len(self.data['Data'].filter(like=column, axis=1).columns)>1:#We have replicates as columns
                self.data['Data']['{} Mean'.format(column)]=self.data['Data'].filter(like=column, axis=1).mean(axis=1)
                self.data['Data']['{} LTB'.format(column)]=self.data['Data'].filter(like=column, axis=1).apply(lib.sn_calc.larger, axis=1)
                ### Check if there are issues in the actual calculations for these two, since they seem to be negative
                self.data['Data']['{} STB'.format(column)]=self.data['Data'].filter(like=column, axis=1).apply(lib.sn_calc.smaller, axis=1)
                self.data['Data']['{} NTB'.format(column)]=self.data['Data'].filter(like=column, axis=1).apply(lib.sn_calc.nominal, axis=1)
            elif self.data['Data'][column].iloc[0].endsith('.txt', '.tsv', '.csv'):
                ### It's a file, call the appropriate function:
                continue
            else:
                continue

        # print(self.data['Data'])
# print(lib.parseOA.peek_line(open(sys.argv[1], 'r')).strip('\w'))
test = taguchiOA(sys.argv[1], sys.argv[2])
test.merge_replicates()
test.calc_values('LTB')
print(test.data['LTB'])