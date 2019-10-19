import sys
sys.path.append('Phase1-FindSimilarCompetitionRegions/processIncomingZip/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/findClosest/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/water/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/demographics/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/manipulation_scripts/')
sys.path.append('Phase0-DefineCompetitionRegions/03-ParseUserZip/')
sys.path.append('private')

import get_centroid_addresses as gca
import extract_lat_lon as ell
import process_incoming_zip as piz
import find_closest as fc
import pandas as pd
import numpy as np

data_path = 'Phase1-FindSimilarCompetitionRegions/data/'

def zip_to_similar(zipcode):

  centroids = pd.read_csv(data_path + 'aggregated_data.csv', dtype = {'zipcode': str}) 

  user_summary, user_data = piz.process_incoming_zip(zipcode)

  ## catch bad zip codes
  if type(user_summary) is str:
    return user_summary

  user_summary['label'] = np.nan
  user_summary = gca.get_addresses(user_summary)

  print('User Input: \n{}\n'.format(user_summary))
  print('Output: \n')
  results = fc.compute_similarity(user_data, centroids)

  centroids_summary = pd.read_csv(data_path + 'centroid_data_with_summary.csv', dtype = {'zipcode': str})

  formatted_results = []

  '''
  for index, result in results.iterrows():
    temp = ell.extract_lat_lon(result['zipcode'])
    del(temp['geopoint'])
    formatted_results.append(temp)
  '''

  formatted_results = centroids_summary[centroids_summary['label'].isin(results.loc[:,'label'])]

  #formatted_results = pd.DataFrame(formatted_results)[['city', 'latitude', 'longitude', 'state_long', 'zipcode', 'label', 'total_water_count', 'median_age', 'total_population']]#.\
  #rename(columns = {'city': 'Matching City', 'latitude': 'Latitude', 'longitude': 'Longitude', 'state': 'State', 'zip': 'Zip'})

  user_summary['id'] = 'user'
  formatted_results['id'] = ['competition']*3
  formatted_results = pd.concat([user_summary, formatted_results]).reset_index()


  return formatted_results

'''

if __name__ == '__main__':
  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: user zipcode')
    sys.exit(1)

  zipcode = args[0]

  print(zip_to_similar(zipcode))

'''