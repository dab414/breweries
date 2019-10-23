import sys
import pandas as pd


def flatten_reviews(d):

  out = []

  for row in d:

    del row['beers']
    brewery_keys = [x for x in row.keys() if x != 'reviews']

    if row['reviews']:

      for beer in row['reviews']:
        new_row = {}

        for k in brewery_keys:
          new_row[k] = row[k]

        for obs in beer:
          new_row.update({'review_{}'.format(obs).lower(): beer[obs]})

        out.append(new_row)



  return out






if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: ratebeer_compiled.txt')
    sys.exit(1)

  file = args[0]

  d = eval(open(file, 'r').read())

  out = flatten_reviews(d)

  file = open('../data/ratebeer/ratebeer_reviews.txt','w')
  file.write(str(out))
  file.close()

