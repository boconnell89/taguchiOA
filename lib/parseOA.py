import pandas as pd

def peek_line(f):
    """Gets us a first line"""
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

def parse(OA):
    """Parses an orthagonal array into a pandas data table and returns it.
    Preferred Formats are either an excel file, the university of york format, or else Neil Sloane's format from http://neilsloane.com/oadir/"""
    if not OA.endswith(".xls") or not OA.endswith(".xlsx"):
        h=open(OA, 'r')
        R=peek_line(h)
        if R.startswith('X'): # Univ. York format
            OAd = pd.read_csv(OA, sep='\t', skiprows=3, header=None, names = range(len(R.strip('\t'))))
            # Set the second row as the index
            # OAd.set_index(1, inplace=True)

        elif R.startswith('0') or R.startswith('1'): # Sloane format
            # print('Sloane format', len(R.strip()))
            if ',' in R:
                OAd = pd.read_csv(OA, header=None, names = range(len(R.strip(','))))
            else:
                OAd = pd.read_table(OA, header=None, names = range(len(R.strip('\t'))))
            if (OAd == 0).any().any():
                # Increment all values by 1
                OAd = OAd + 1
        elif R.startswith('-1'): #https://develve.net/Orthogonal%20Array.html
            OAd = pd.read_table(OA, header=None, names = range(len(R.strip('\t'))))
            OAd = OAd + 2
        elif R.startswith('+') or R.startswith('-'): # Annoying format
            OAd=pd.read_csv(OA, header=None, names=list(range(1, len(R.strip())+1)))
            OAd.replace({'+': 2, '-': 1}, inplace=True)
        # print(OAd)
        return OAd.dropna(axis=1)

# def parseData(dataFile):
#     """Parses a data file (xlsx or xls format), where the first n columns are the factors, and the remaining columns are the responses. Note that different replicates are indicated with Response.1, response.2, etc."""
#     return dataFile    