import urllib.parse
import sys
import requests
sys.path.append('../../private/')
from loquate_key import *

def geocode_breweries(d):
  ## input: [(brewery_id, address), ...]

  out = {}

  base = 'https://api.addressy.com/Geocoding/International/Geocode/v1.10/json3.ws'
  country = 'Country=US'
  key = 'Key={}'.format(api_key)

  for count, brewery in enumerate(d):

    location = 'Location=' + urllib.parse.quote(brewery[1])
    query = base + '?' + '&'.join([country, key, location])

    result = requests.get(query)

    result = eval(result.text)['Items'][0]

    try:
      out[brewery[0]] = {'latitude': result['Latitude'], 'longitude': result['Longitude']}
    except:
      pass

    if not count % 100:
      print('Parsing brewery {} of {}.\n'.format(count, len(d)))

  return out




if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: brewery_name_address.txt')
    sys.exit(1)

  file = args[0]

  print(file)

  d = eval(open(file, 'rb').read())



  out = geocode_breweries(d)

  file = open('../data/twitter/geocoded_breweries.txt', 'w')
  file.write(str(out))
  file.close()