from . import sn_calc
import pandas as pd

""" Imports an experiment as an Excel File with 3 sheets:
    1. 'Set-up' or 'Setup' or Set up': Has the different levels used for each factor, while the first cell of each column is the name of the factor.
    2. 'Results' or 'Data': the response data, with 1 line per run, multiple cells allowed per line if there are replicates.
    3. 'Analysis': Uses the same factor names, and beneath each includes rows indicating which analyses should be used, specifically:
        -   Mean for level average analysis
        -   LTB for Larger the better
        -   STB for smaller the better
        -   NTB for nominal the best
        """
def parseExperiment(fileName):
    exp=pd.ExcelFile(fileName)
    try:
        setUp=exp.parse('Set-up')
    except ValueError:
        try:
            setUp=exp.parse('Setup')
        except ValueError:
            setUp=exp.parse('Set up')
    try:
        results=exp.parse('Results')
    except ValueError:
        results=exp.parse('Data')
    analysis=exp.parse('Analysis')
    return {'Factors':setUp, 'Data':results, 'Setup':analysis}