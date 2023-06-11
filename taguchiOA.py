import numpy as np
import pandas as pd
import math
import lib
import sys
import os
import re
from pandas.api.types import is_integer_dtype

class taguchiOA:
    def __init__(self, OA, experiment=''):
        self.OA = lib.parseOA.parse(OA)
        # print(self.OA)
        self.data=lib.parseExperiment.parseExperiment(experiment)
        # Create a list of common column names between OA and Setup
        for i, column in enumerate(self.data['Factors'].columns):
            self.OA.rename(columns={i: column}, inplace=True)
        

    def calc_values(self):
        """Calculates the Level Average, and S/N indicated in data["Data"]. Suffix= Mean, LTB, STB, or NTB"""
        
        self.data['Data'].replace([np.inf, -np.inf], 0.0, inplace=True)
        for column in self.data['Factors'].columns:
            if is_integer_dtype(self.data['Factors'][column]):
            #    print(column)
                self.data['Factors'][column]=self.data['Factors'][column].astype(float)

        options=['Mean', 'LTB', 'STB', 'NTB']
        # print(self.data['Factors'], self.data['Data'],'\n', self.data['Setup'],'\n', self.OA)
        for option in options:
            self.data[option]={}
            for Response in self.data['Setup']:
                # print(option,Response, self.data['Setup'][Response])
                if option in self.data['Setup'][Response].values:
                    self.data[option][Response]=lib.LAA.LAA(self.OA, self.data['Data'].filter(like=option, axis=1), self.data['Factors'], Response, option)
        # self.data[options]=lib.LAA.LAA(self.OA, self.data['Data'], self.data['Factors'], self.data['Setup'], option)
        # print(self.data['LTB'])
        print('MEAN')
        print(self.data['Mean'])
        print('\nLTB')
        print(self.data['LTB'])
        print('\nNTB')
        print(self.data['NTB'])
        
    def merge_replicates(self):
        """merges replicates. """
        for column in self.data['Setup'].columns: #Get different basic response variables
            if len(self.data['Data'].filter(like=column, axis=1).columns)>1:#We have replicates as columns
                tmp=self.data['Data'].filter(like=column, axis=1)
                self.data['Data']['{} Mean'.format(column)]=tmp.mean(axis=1)
                if 'LTB' in self.data['Setup'][column].values:
                    self.data['Data']['{} LTB'.format(column)]=tmp.apply(lib.sn_calc.larger, axis=1)
                ### Check if there are issues in the actual calculations for these two, since they seem to be negative
                if 'STB' in self.data['Setup'][column].values:
                    self.data['Data']['{} STB'.format(column)]=tmp.apply(lib.sn_calc.smaller, axis=1)
                if 'NTB' in self.data['Setup'][column].values:
                    self.data['Data']['{} NTB'.format(column)]=tmp.apply(lib.sn_calc.nominal, axis=1)
                # print(list(self.data['Data'].filter(regex='\.')))
            elif  self.data['Data'][column].dtype!=np.float64 and self.data['Data'][column].iloc[0].endsith('.txt', '.tsv', '.csv'):
                ### It's a file, call the appropriate function:
                continue
            else:
                self.data['Data']['{} Mean'.format(column)]=self.data['Data']
        for col in self.data['Data'].columns:
            if re.search(r'\d+$', col):
                del self.data['Data'][col]
        
       
# print(lib.parseOA.peek_line(open(sys.argv[1], 'r')).strip('\w'))
test = taguchiOA(sys.argv[1], sys.argv[2])
# print(test.data['Setup'])
test.merge_replicates()
# print(test.data['Data'].filter(like='LTB'))
# print(test.data)
test.calc_values()
print(test.data['Factors'])
# test.calc_values('LTB')

# print(test.data['Mean'])
# print(test.data['LTB'])