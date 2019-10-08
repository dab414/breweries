import sys 
sys.path.append('../../organizational_scripts/')

from set_wd import set_wd
import pandas as pd


root = set_wd()

def txt_to_csv(t):

  d = pd.DataFrame(t)

  d = d.rename(columns = {'Zip': 'zipcode'}).astype({'zipcode': str}).dropna(subset = ['zipcode'])


  d = d[d['zipcode'].map(len) == 5]

  return d


if __name__ == '__main__':

  
  t = eval(open('../data/centroid_data.txt', 'r').read())

  out = txt_to_csv(t)

  out.to_csv('../centroid_data.csv', index = False)