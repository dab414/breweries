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



def harvest_users(guide_data):

  out = []

  for count, brewery in enumerate(guide_data):
    try:
      out.append((brewery[0], api.GetUser(screen_name = brewery[1])))

    except twitter.error.TwitterError as t:
      if t.message == 'User not found.':
        print('User {} not found\n'.format(brewery[1]))
        pass

    except:
      print('Something other than user not found happened when calling the api')

    if not count % 10:
      print('Scraping: {}'.format(brewery[1]))
      print('{} / {}\n\n'.format(count, len(guide_data)))

  return out


if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: ratebeer_compiled.txt')
    sys.exit(1)

  guide_data = eval(open(args[0], 'r').read())

  guide_data = [(x['brewery_id'], x['twitter_link']) for x in guide_data if x['twitter_link']]

  guide_data = [(x[0], re.search(r'twitter\.com/(.*)', x[1]).group(1)) for x in guide_data]



  ## prune what's already been scraped
  cache_path = '../data/twitter/cache/get_user_cache.dll'
  if os.path.exists(cache_path):
    prev_data = dill.load(open(cache_path, 'rb'))
    prev_screen_names = [x.screen_name for x in prev_data]
    guide_data = [x for x in guide_data if x[1] not in prev_screen_names]


  out = harvest_users(guide_data)

  dill.dump(out, open('../data/twitter/brewery_accounts.dll', 'wb'))

