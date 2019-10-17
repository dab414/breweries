import urllib.parse
import sys
import requests
sys.path.append('../../private/')
from google_geocoding import *
import json

def geocode_breweries(d):
  ## input: [(brewery_id, address), ...]

  out = {}

  base = 'https://maps.googleapis.com/maps/api/geocode/json'
  key = 'key={}'.format(api_key)

  for count, brewery in enumerate(d):

    address = 'address=' + brewery[1].replace(' ', '+')
    query = base + '?' + '&'.join([address, key])

    result = requests.get(query)

    #result = eval(result.text)['results']['geometry']
    result = json.loads(result.text)

    if result['results']:
      result = result['results'][0]['geometry']['location']
    else:
      out[brewery[0]] = None
      pass

    try:
      out[brewery[0]] = {'latitude': result['lat'], 'longitude': result['lng']}
    except:
      pass

    if not count % 10:
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