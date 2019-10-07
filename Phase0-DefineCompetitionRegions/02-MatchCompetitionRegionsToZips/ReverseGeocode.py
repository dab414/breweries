## Objective:
  ## I WILL need to get zips for *all* competition areas in order to collect zip data on each
  ## Just make min 3 requests instead of > 150
## https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP.aspx

import requests
import re
import sys

api_key_path = '/home/dave/OneDrive/Professional Development/Fellowships/incubator/capstoneProject/private/convertLatLonToZipAccount.txt'


def main(lat_lon_list):
  ## lat_lon is a list of ((lat, lon), label) nested tuples
    ## lat_lon will have length greater than n_similar, but only n_similar will be required for output
  ## returns list of dicts of len n_similar where each dict is data for a lat_lon pair


  ## bring in api key
  apiKey = open(api_key_path).read()
  apiKey = re.search(r'api key:\ (.*)', apiKey).group(1)
  apiKey = 'apiKey=' + apiKey
  version = 'version=4.10'
  includeHeader = 'includeHeader=true'

  ## output will be a list of dicts where keys are the headers
  out = []

  query = ('&').join([apiKey, version, includeHeader])

  for index, lat_lon in enumerate(lat_lon_list):
    
    lat_lon_coords = lat_lon[0]
    label = lat_lon[1]

    result = request_location(lat_lon_coords, query)

    if result:
      result['label'] = label
      result['latitude'] = lat_lon_coords[0]
      result['longitude'] = lat_lon_coords[1]
      out.append(result)


    if not index % 10:
      print('Parsing cluster {} of {}.'.format(index, len(lat_lon_list)))

  return out


def request_location(lat_lon, query):
  ## takes as input a lat_lon tuple
  ## if request is successful, returns list of dicts where each dict is data for a lat_lon pair
  ## else, returns ... something else

  lat = 'lat={}'.format(lat_lon[0])
  lon = 'lon={}'.format(lat_lon[1])

  base_url = 'https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?'

  query = '&'.join([query, lat, lon])

  ## this line gives a list with len 2 where the first element are headers and the next is the data
  response = requests.get(base_url + query).text.strip().split('\n')

  ## if request failed
  if len(response) == 1:
    return ''

  headers = response[0].split(',')
  data = response[1].split(',')

  d = {}

  for header, datum in zip(headers, data):
    d[header.strip()] = datum

  return d


if __name__ == '__main__':

  ## takes as command line arg a file name containing a list of lat_lon tuples

  args = sys.argv[1:]

  if not args or len(args) > 1:
    print('You must pass the name of one file to parse.')
    sys.exit(1)

  file = args[0]

  lat_lon_list = []

  for line in open(file, 'r'):
    lat_lon_list.append(eval(line.strip()))

  print(main(lat_lon_list))

