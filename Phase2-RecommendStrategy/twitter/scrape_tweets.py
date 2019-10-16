import re
import datetime
import time
import os
import twitter
import sys
sys.path.append('../../private/')
from twitter_keys import *
import dill

api = twitter.api.Api(consumer_key = consumer_key, 
  consumer_secret = consumer_secret, 
  access_token_key = access_token_key, 
  access_token_secret = access_token_secret,
  sleep_on_rate_limit = True)   



def harvest_tweets(guide_data):

  out = []

  for count, brewery in enumerate(guide_data):
    try:
      query = 'q="' + brewery[1] + '"'
      since = '2019-01-01'
      out.append((brewery[0], api.GetSearch(raw_query = query, count = 100, since = since)))


    except twitter.error.TwitterError as t:
      if t.message == 'User not found.':
        print('User {} not found\n'.format(brewery[1]))
        pass

    except:
      print('Something other than user not found happened when calling the api')

    if count and not count % 10:
      cache(out)
      out = []
      print('Scraping: {}'.format(brewery[1]))
      print('{} / {}\n\n'.format(count, len(guide_data)))

  return out


def cache(out):

  cache_dir = '../data/twitter/cache/breweries_tweets_cache.dll'

  prev_data = []

  if os.path.exists(cache_dir):
    prev_data = dill.load(open(cache_dir, 'rb'))
    prev_data.extend(out)

  if not prev_data:
    prev_data = out


  dill.dump(prev_data, open(cache_dir, 'wb'))




if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: breweries_names.txt')
    sys.exit(1)

  guide_data = eval(open(args[0], 'r').read())

  guide_data = [x for x in guide_data if x[1]]

  ## prune what's already been scraped
  cache_path = '../data/twitter/cache/breweries_tweets_cache.dll'
  if os.path.exists(cache_path):
    prev_data = dill.load(open(cache_path, 'rb'))
    prev_ids = [x[0] for x in prev_data]
    guide_data = [x for x in guide_data if x[0] not in prev_ids]


  out = harvest_tweets(guide_data[:50])

  if os.path.exists(cache_path):
    prev_data = dill.load(open(cache_path, 'rb'))
    prev_data.extend(out)

  dill.dump(prev_data, open('../data/twitter/breweries_tweets.dll', 'wb'))

