import pandas as pd
import numpy as np
import sys


def convert_csv(d):
  out = d['zipcode'].dropna().to_numpy()
  return list(out)

if __name__ == '__main__':
  
  args = sys.argv[1:]
  
  if len(args) != 1:
    print('Usage: centroid_data.csv')
    sys.exit(1)

  in_data = args[0]

  d = pd.read_csv(in_data, dtype = {'zipcode': str})
  out = convert_csv(d)
  f = open('../data/zips_list.txt', 'w')
  f.write(str(out))
  f.close()