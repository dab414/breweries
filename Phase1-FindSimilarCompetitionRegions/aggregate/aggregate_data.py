import pandas as pd
import sys
import numpy as np




if __name__ == '__main__':
  args = sys.argv[1:]

  if len(args) < 2:
    print('Usage: base_zip_data.csv join_zip_data.csv; base needs to be water data')
    sys.exit(1)

  base_data = pd.read_csv(args[0], dtype = {'zipcode': str})
  

  base_data = pd.get_dummies(base_data, columns = ['contam']).groupby('zipcode').sum()
  #base_data['zipcode'] = base_data.index
  base_data = base_data.reset_index()
  print(base_data.head())

  for arg in args[1:]:
    join_data = pd.read_csv(arg, dtype = {'zipcode': str})
    if arg == '../data/centroid_data.csv':
      join_data = join_data[['zipcode', 'label']]
    base_data = base_data.merge(join_data)

  base_data.to_csv('../data/aggregated_data.csv', index = False)