import sys
import pandas as pd
import numpy as np
sys.path.append('water/')
sys.path.append('demographics/')
sys.path.append('../Phase0-DefineCompetitionRegions/03-ParseUserZip/')
#sys.path.append('../manipulation_scripts/')
import preprocess_water as pw
import census_scrape as cs
import scrape_ewg as se
import extract_lat_lon as ell
#import centroid_txt_to_csv as ctc

aggregated_data_path = 'Phase1-FindSimilarCompetitionRegions/data/aggregated_data.csv'
water_columns_path = 'Phase1-FindSimilarCompetitionRegions/data/water_columns.txt'


def get_water_data(user_summary):
  ## takes in df with one row with location data about user input
  ## returns a dict where keys are water col names and values are counts of the contams

  target_water_columns = eval(open(water_columns_path, 'r').read())

  water_counts = {}

  for e in target_water_columns:
    water_counts[e] = 0

  user_water = se.scrape_ewg(user_summary.rename(columns = {'zipcode':'zip'})[['zip', 'state_id']])

  total_count = 0

  for city in user_water:
    for contam in city['contaminants_above_hbl']:
      if 'contam_' + contam in water_counts:
        water_counts['contam_' + contam] += 1
        total_count += 1
    for contam in city['contaminants_other']:
      if 'contam_' + contam in water_counts:
        water_counts['contam_' + contam] += 1
        total_count += 1


  return water_counts, total_count



def process_incoming_zip(user_zip):

  ## takes as input zipcode from user
  ## returns a one-line df with same columns as centroid data
    ## elements are *counts*

  ## translate zip code to location
  user_summary = ell.extract_lat_lon(user_zip)

  if user_summary == 'ZIPCODE INVALID':
    return 'The zipcode you entered is invalid. Please enter a valid US zipcode.', 1
    

  del(user_summary['geopoint'])
  user_summary = pd.DataFrame(user_summary, index = [0])
  user_summary = user_summary.rename(columns = {'zip': 'zipcode', 'state': 'state_id'}).astype({'zipcode': str}).dropna(subset = ['zipcode'])
  user_summary = user_summary[user_summary['zipcode'].map(len) == 5]


  ## get water data -- comes in as dict where keys are cols and vals are counts
  user_water_dict, total_water_count = get_water_data(user_summary)
  user_water = pd.DataFrame(user_water_dict, index = [0])

  ## get census data -- comes in as df with one row
  user_demo = cs.webScrape([user_zip]).drop('zipcode', axis = 1)
  ## throw total population on user_summary
  user_summary = pd.concat([user_summary, user_demo[['total', 'median_age']]], axis = 1)
  user_summary = user_summary.rename(columns = {'total': 'total_population'})
  user_summary['total_water_count'] = total_water_count
  user_demo = user_demo.drop('median_age', axis = 1)

  user_base = user_summary[['zipcode', 'latitude', 'longitude']]

  user_data = pd.concat([user_base, user_water, user_demo], axis = 1)

  return user_summary, user_data


if __name__ == '__main__':

  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: zipcode')
    sys.exit(1)

  user_zip = args[0]

  print(process_incoming_zip(user_zip)[0])