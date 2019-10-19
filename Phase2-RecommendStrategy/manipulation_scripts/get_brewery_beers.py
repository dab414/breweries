import sys


def extract_beers(files):

  out = []

  for count, file in enumerate(files):

    d = eval(open(file, 'r').read())
    print('Opened file {}'.format(count))

    for row in d:
      out.append(repair_beers(row))

  return out



def repair_beers(row):

  beers = row['beers']
  out_beers = []

  already_present = {}

  for beer in beers:
    
    if beer['Name'] not in already_present:
      already_present[beer['Name']] = 1
      out_beers.append(beer)

  row['beers'] = out_beers

  return row













if __name__ == '__main__':

  args = sys.argv[1:]

  if len(args) != 3:
    print('Usage: ratebeer_data.txt')
    sys.exit(1)

  breweries_beers = extract_beers(args)

  file = open('../data/ratebeer/breweries_beers.txt', 'w')
  file.write(str(breweries_beers))
  file.close()