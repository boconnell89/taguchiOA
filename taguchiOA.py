import numpy as np
import pandas as pd
import math
import lib
import sys
import os
import re
from pandas.api.types import is_integer_dtype
import seaborn as sns
from matplotlib import pyplot as plt
class taguchiOA:
    def __init__(self, OA, experiment=''):
        self.OA = lib.parseOA.parse(OA)
        # print(self.OA)
        self.data=lib.parseExperiment.parseExperiment(experiment)
        # Create a list of common column names between OA and Setup
        for i, column in enumerate(self.data['Factors'].columns):
            self.OA.rename(columns={i: column}, inplace=True)
        
        ### What are the Analysis options
        self.analyses=['Mean', 'LTB', 'STB', 'NTB']

        ### Just so we don't have things being annoying
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def calc_values(self):
        """Calculates the Level Average, and S/N indicated in data["Data"]. Suffix= Mean, LTB, STB, or NTB"""
        
        self.data['Data'].replace([np.inf, -np.inf], 0.0, inplace=True)
        for column in self.data['Factors'].columns:
            if is_integer_dtype(self.data['Factors'][column]):
            #    print(column)
                self.data['Factors'][column]=self.data['Factors'][column].astype(float)

        options=self.analyses
        # print(self.data['Factors'], self.data['Data'],'\n', self.data['Setup'],'\n', self.OA)
        for option in options:
            self.data[option]={}
            for Response in self.data['Setup']:
                # print(option,Response, self.data['Setup'][Response])
                if option in self.data['Setup'][Response].values:
                    self.data[option][Response]=lib.LAA.LAA(self.OA, self.data['Data'].filter(like=option, axis=1), self.data['Factors'], Response, option)
        
    def merge_replicates(self):
        """merges replicates. Also calculates the S/N values where appropriate"""
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

    def plot_levels(self, path='./'):
        """Plots facetgrids for each Response variable. Can be given a path to write out to
        TODO: exempt the interaction columns?
        """ 
        for Analysis in self.analyses:   
            for Response in test.data[Analysis]:

                #Melt and concat the levels for the factors with the response values
                Resp=test.data[Analysis][Response].melt(var_name='Column', value_name=Analysis)
                Factors=test.data['Factors'].melt(var_name='Column', value_name='Factor')
                combined_df=pd.concat([Resp, Factors['Factor']], axis=1)

                # Make a facetgrid
                g = sns.FacetGrid(combined_df, col='Column', col_wrap=4, height=4)

                # Create the point plot for each unique value in 'Column'
                g.map(sns.pointplot, 'Factor', Analysis)

                # Set the axis labels
                g.set_axis_labels('Factor', Analysis)

                # Set the plot title for each facet
                g.set_titles('{col_name}')
                g.fig.suptitle('{},{}'.format(Response,Analysis ), fontsize=16)

                # Give more space for the x-ticks
                plt.subplots_adjust(hspace=0.6)

                # Adjust the plot layout
                plt.tight_layout()
                for ax in g.axes.flat:
                    ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
                    ax.xaxis.set_tick_params(pad=10)
                # Show the plot
                plt.savefig('{}{}.{}.pdf'.format(path, Response, Analysis))
                plt.savefig('{}{}.{}.png'.format(path, Response, Analysis))


### Create the experiment:
test = taguchiOA(sys.argv[1], sys.argv[2])

### Merge Replicates:
test.merge_replicates()

### Calculate the LAA's:
test.calc_values()

### Plot everything to the specified directory
test.plot_levels(sys.argv[3])