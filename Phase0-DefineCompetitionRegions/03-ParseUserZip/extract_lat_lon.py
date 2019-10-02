import sys
import requests


def extract_lat_lon(userZip):

  base = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&facet=state&facet=timezone&facet=dst&q='

  data = eval(requests.get(base + userZip).text)


  if data['nhits']:
    return data['records'][0]['fields']

  return 'ZIPCODE INVALID'



if __name__ == '__main__':

  args = sys.argv[1:]
  
  if len(args) > 1:
    print('Usage: zipcode')
    sys.exit(1)



  print(extract_lat_lon(args[0]))