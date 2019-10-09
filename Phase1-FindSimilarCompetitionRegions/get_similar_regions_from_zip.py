import sys
sys.path.append('processIncomingZip/')
sys.path.append('findClosest/')
sys.path.append('water/')
sys.path.append('demographics/')
sys.path.append('../Phase0-DefineCompetitionRegions/03-ParseUserZip/')
import process_incoming_zip as piz
import find_closest as fc
import pandas as pd



if __name__ == '__main__':
  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: user zipcode')
    sys.exit(1)

  centroids = pd.read_csv('data/aggregated_data.csv', dtype = {'zipcode': str})  

  zipcode = args[0]

  user_data = piz.process_incoming_zip(zipcode)

  print('User Input: \n{}\n'.format(user_data[['zipcode', 'latitude', 'longitude']]))
  print('Output: \n')
  print(fc.compute_similarity(user_data, centroids))


