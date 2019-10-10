import sys
sys.path.append('Phase1-FindSimilarCompetitionRegions/processIncomingZip/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/findClosest/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/water/')
sys.path.append('Phase1-FindSimilarCompetitionRegions/demographics/')
sys.path.append('Phase0-DefineCompetitionRegions/03-ParseUserZip/')
import extract_lat_lon as ell
import process_incoming_zip as piz
import find_closest as fc
import pandas as pd


def zip_to_similar(zipcode):

  centroids = pd.read_csv('Phase1-FindSimilarCompetitionRegions/data/aggregated_data.csv', dtype = {'zipcode': str}) 

  user_base, user_data = piz.process_incoming_zip(zipcode)

  ## catch bad zip codes
  if type(user_base) is str:
    return user_base


  print('User Input: \n{}\n'.format(user_base))
  print('Output: \n')
  results = fc.compute_similarity(user_data, centroids)

  formatted_results = []

  for index, result in results.iterrows():
    temp = ell.extract_lat_lon(result['zipcode'])
    del(temp['geopoint'])
    formatted_results.append(temp)

  formatted_results = pd.DataFrame(formatted_results)[['city', 'latitude', 'longitude', 'state', 'zip']].\
  rename(columns = {'city': 'Matching City', 'latitude': 'Latitude', 'longitude': 'Longitude', 'state': 'State', 'zip': 'Zip'})

  return pd.DataFrame(formatted_results)



# if __name__ == '__main__':
#   args = sys.argv[1:]

#   if len(args) != 1:
#     print('Usage: user zipcode')
#     sys.exit(1)

#   zipcode = args[0]

#   zip_to_similar(zipcode)

