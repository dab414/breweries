import sys 
sys.path.append('../../organizational_scripts/')

import pandas as pd




def txt_to_csv(t):

  print('Len text: {}'.format(len(t)))

  d = pd.DataFrame(t, dtype = str)



  d = d.rename(columns = {'Zip': 'zipcode'}).astype({'zipcode': str}).dropna(subset = ['zipcode'])
  print('Len df: {}'.format(d.shape))

  d = d[d['zipcode'].map(len) == 5]
  print('Len df after zip trim: {}'.format(d.shape))


  return d


if __name__ == '__main__':

  
  t = eval(open('../data/centroid_data.txt', 'r').read())

  out = txt_to_csv(t)

  print([x for x in out['zipcode'].values if len(x) != 5])

  out.to_csv('../data/centroid_data.csv', index = False)