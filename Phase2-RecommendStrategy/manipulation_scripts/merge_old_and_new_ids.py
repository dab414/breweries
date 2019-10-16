import sys
import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
  ## from: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
  return SequenceMatcher(None, a, b).ratio()




def merge_data(old_data, new_data):

  ## this is going to be expensive...
  ## i need to match second element of new data with first element of old
  ## this is gonna be SO messy

  out = []


  for old_brewery in old_data[1999:]:
    matches = []
    print('\n')
    print(old_brewery)
    print('\n')

    for new_brewery in new_data:
      similarity = similar(new_brewery[1], old_brewery[0])
      matches.append(tuple(new_brewery) + (similarity,))

    print(sorted(matches, key = lambda x: -x[-1])[:5])
    sys.exit(1)

  




if __name__ == '__main__':

  args = sys.argv[1:]

  # if not args:
  #   print('Usage: old_data.csv new_data.txt')
  #   sys.exit(1)

  old_data = pd.read_csv('../../Phase0-DefineCompetitionRegions/data/breweries.csv')
  new_data = eval(open('../data/twitter/breweries_names.txt', 'r').read())

  old_data = [(x[0], x[1], x[2]) for x in old_data[['name', 'latitude', 'longitude']].values]

  merge_data(old_data, new_data)