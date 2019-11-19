import requests
from bs4 import BeautifulSoup
import json
import sys
from get_similar_regions_from_zip import zip_to_similar


def get_random_zip():

  ran_zip = []

  while not ran_zip:
    page = requests.get('https://www.bestrandoms.com/random-zipcode').text
    soup = BeautifulSoup(page, 'lxml')

    ran_zip = soup.select('p.text-center')[1].text

  return ran_zip


def get_nearby_zips(target_zip, n_neighbors  = 10):
  key = 'YL6ZliVWh4ChhYOTdDOXjFchVEKS02VLPMXUNENzgPM3kijjZl6LVNocRc4pCw1e'
  url = 'https://www.zipcodeapi.com/rest/{}/radius.json/{}/50/mile'.format(key, target_zip)
  response = requests.get(url).text
  zip_data = json.loads(response)['zip_codes'][:n_neighbors]
  nearby_zips = []

  for e in zip_data:
    nearby_zips.append(e['zip_code'])

  return nearby_zips

def run_matcher(machine_id):

  d = []

  ## run the random condition
  if machine_id == 'desktop':
    for i in range(500):
      condition = 'random'
      
      
      result_df = ''
      while type(result_df) is str:
        input_zip = get_random_zip()
        result_df = zip_to_similar(input_zip)
      
      output_latlon = result_df.loc[1, ['latitude', 'longitude']]

      out = {'id': i, 'condition': condition, 'input_zip': input_zip, 'output_lat': output_latlon['latitude'], 'output_lon': output_latlon['longitude']}
      d.append(out)

      if i and not i % 20:
        print('Random condition. Processing brewery {} of 500 (in this condition).'.format(i))
        print('\n')
        print(d[-15:])

  ## run the clustered condition
  if machine_id == 'laptop':
    for count, outer in enumerate(range(50)):
      random_zip = get_random_zip()
      nearby_zips = get_nearby_zips(random_zip)
      iden = count + 500

      for zipcode in nearby_zips:
        condition = 'grouped'

        
        result_df = zip_to_similar(zipcode)

        ## bad zipcodes
        if type(result_df) is str:
          continue

        output_latlon = result_df.loc[1, ['latitude', 'longitude']]

        out = {'id': iden, 'condition': condition, 'input_zip': zipcode, 'output_lat': output_latlon['latitude'], 'output_lon': output_latlon['longitude']}
        d.append(out)

      if not count % 2:
        print('Grouped condition. Processing batch {} of 50 (in this condition).'.format(count))
        print('\n')
        print(d[-15:])


  return d



if __name__ == '__main__':

  args = sys.argv[1:]
  if not args:
    print('Usage: machine_id')
    sys.exit(1)

  machine_id = args[0]

  result = run_matcher(machine_id) 

  f = open('validate_matcher/result_{}.txt'.format(machine_id), 'w')
  f.write(str(result))
  f.close()