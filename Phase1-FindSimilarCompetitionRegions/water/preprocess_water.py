import pandas as pd
import numpy as np
import sys



def preprocess_water(d):

  water_dict = {}

  for index, row in d.iterrows():
    zipcode = row['zipcode']
    contam = eval(row['contaminants_above_hbl']) + eval(row['contaminants_other'])

    if zipcode not in water_dict:
      water_dict[zipcode] = contam

    else:
      water_dict[zipcode] += contam

  df = []

  for zipcode in water_dict:

    for contam in water_dict[zipcode]:
      df.append({'zipcode': zipcode, 'contam': contam})


  return(pd.DataFrame(df))


if __name__ == '__main__':

  args = sys.argv[1:]
  

  if len(args) != 1:
    print('Usage: water_by_zip_raw.csv')
    sys.exit(1)

  d = pd.read_csv(args[0], dtype = {'zip': str}).rename(columns = {'zip': 'zipcode'})

  out = preprocess_water(d)

  out.to_csv('../data/water_by_zip.csv', index = False)