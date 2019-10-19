import sys
import pandas as pd


def flatten_beers(d):

  out = []

  for row in d:

    del row['reviews']
    brewery_keys = [x for x in row.keys() if x != 'beers']

    for beer in row['beers']:
      new_row = {}

      for k in brewery_keys:
        new_row[k] = row[k]

      for obs in beer:
        new_row.update({'beer_{}'.format(obs).lower(): beer[obs]})

      out.append(new_row)



  return out






if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: ratebeer_compiled.txt')
    sys.exit(1)

  file = args[0]

  d = eval(open(file, 'r').read())

  out = flatten_beers(d)

  file = open('../data/ratebeer/ratebeer_beers.txt','w')
  file.write(str(out))
  file.close()

