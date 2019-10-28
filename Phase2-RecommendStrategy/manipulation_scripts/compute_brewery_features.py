import sys
import dill
import numpy as np
import pandas as pd

def compile_data(ratebeer, geocodes, twitter):

  out = []

  ## convert to flat dict
  t = [{x[0]: x[1]} for x in twitter]
  twitter = {}
  for brewery in t:
    twitter.update(brewery)


  for row in ratebeer:
    new_row = {}
    for k in row:
      if k != 'reviews' and k != 'beers':
        new_row.update({k: row[k]})
    
    ## GEOCODES
    if new_row['brewery_id'] in geocodes and geocodes[new_row['brewery_id']]:
      new_row['latitude'] = geocodes[new_row['brewery_id']]['latitude']
      new_row['longitude'] = geocodes[new_row['brewery_id']]['longitude']
    else:
      new_row['latitude'] = None
      new_row['longitude'] = None

    
    ## SUMMARIZE BEER DATA
    new_row['beer_count'] = len(row['beers']) if row['beers'] else None
    new_row['review_count'] = len(row['reviews']) if row['reviews'] else None

    avg_beer_rating = 0
    
    beer_ratings = np.array([float(x['beer_score']) for x in row['beers'] if x['beer_score']])
    
    if len(beer_ratings):
      new_row['beer_rating_avg'] = beer_ratings.mean()
      new_row['beer_rating_var'] = beer_ratings.var()
      new_row['beer_rating_max'] = beer_ratings.max()
      new_row['beer_rating_min'] = beer_ratings.min()
    else:
      new_row['beer_rating_avg'] = None
      new_row['beer_rating_var'] = None
      new_row['beer_rating_max'] = None
      new_row['beer_rating_min'] = None

    ## TWITTER DATA
    
    if row['brewery_id'] in twitter:
      new_row['twitter_followers_count'] = twitter[row['brewery_id']].followers_count
      new_row['twitter_statuses_count'] = twitter[row['brewery_id']].statuses_count
      new_row['twitter_favorites_count'] = twitter[row['brewery_id']].favourites_count
    else:
      new_row['twitter_followers_count'] = None
      new_row['twitter_statuses_count'] = None
      new_row['twitter_favorites_count'] = None



    out.append(new_row)

  ## filter out commericial breweries
  out = [x for x in out if x['brewery_type'] != 'Commercial Brewery']

  return out



if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: ratebeer_compiled.txt geocoded_breweries.txt brewery_accounts.dll')
    sys.exit(1)

  ratebeer = eval(open(args[0], 'r').read())
  geocodes = eval(open(args[1], 'r').read())
  twitter = dill.load(open(args[2], 'rb'))

  out = compile_data(ratebeer, geocodes, twitter)

  file = open('../data/brewery_features.txt', 'w')
  file.write(str(out))
  file.close()

  pd.DataFrame(out).to_csv('../data/brewery_features_df.csv', index = False)