import json
import sys
import pandas as pd
sys.path.append('../../private/')
from google_geocoding import *
import requests


def get_addresses(d):

  cols = ['zipcode', 'label', 'latitude', 'longitude', 'total_population', 'median_age',\
  'total_water_count']

  base = 'https://maps.googleapis.com/maps/api/geocode/json?'
  key = 'key={}'.format(api_key)

  new_data = []

  for index, row in d.iterrows():
    lat, lon  = row['latitude'], row['longitude']
    latlng = 'latlng={}'.format(','.join([str(lat), str(lon)]))
    query = base + '&'.join([key, latlng])

    page = requests.get(query)

    if page.status_code != 200:
      new_data.append(save_data([None] * 3))
      continue

    address = json.loads(page.text)['results'][0]['address_components']
    city = None
    state_abbrv = None
    state_long = None

    for entry in address:

      if 'locality' in entry['types']:
        city = entry['long_name']
      elif 'administrative_area_level_1' in entry['types']:
        state_abbrv = entry['short_name']
        state_long = entry['long_name']

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

  out.to_csv('../data/centroid_data_with_summary.csv', index = False)