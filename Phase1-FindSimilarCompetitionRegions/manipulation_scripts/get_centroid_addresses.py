import json
import sys
import pandas as pd
sys.path.append('../../private/')
from mapquest_geocoding import *
import requests


def get_addresses(d):

  cols = ['zipcode', 'label', 'latitude', 'longitude', 'total_population', 'median_age',\
  'total_water_count']

  ## update with the mapquest api
  base = 'http://open.mapquestapi.com/geocoding/v1/reverse?'
  key = 'key={}'.format(api_key)
  state_abbreviations = eval(open('Phase1-FindSimilarCompetitionRegions/data/state_abbreviations_dict.txt', 'r').read())

  new_data = []

  for index, row in d.iterrows():
    lat, lon  = row['latitude'], row['longitude']
    latlng = 'location={}'.format(','.join([str(lat), str(lon)]))
    query = base + '&'.join([key, latlng])

    page = requests.get(query)

    if page.status_code != 200:
      new_data.append(save_data([None] * 3))
      continue

    locations = json.loads(page.text)['results'][0]['locations']

    city = None
    state_abbrv = None
    state_long = None

    if locations:

      if 'adminArea5' in locations[0] and locations[0]['adminArea5']:
        city = locations[0]['adminArea5']
      if 'adminArea3' in locations[0] and locations[0]['adminArea3']:
        state_abbrv = locations[0]['adminArea3']
        state_long = state_abbreviations[state_abbrv]
        

    new_data.append(save_data([city, state_abbrv, state_long]))

    
    
  return pd.concat([d[cols], pd.DataFrame(new_data)], axis = 1)
      


def save_data(l):
  out = {}
  keys = ['city', 'state_abbrv', 'state_long']

  for k, e in zip(keys, l):
    out[k] = e

  return out




if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: centroid_data_with_summary.csv')
    sys.exit(1)

  d = pd.read_csv(args[0], dtype = {'zipcode': str})

  out = get_addresses(d)
  print(out)

  #out.to_csv('../data/centroid_data_with_summary.csv', index = False)