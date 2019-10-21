import os
from difflib import SequenceMatcher
import sys
import requests
import urllib
from fake_useragent import UserAgent
import time
import numpy as np
from bs4 import BeautifulSoup
sys.path.append('../untappd/')
from rotate_proxies import RotateProxies

cache_dir = '../data/untappd/cache/'
throttle = 1.5
cache_frequency = 100

def similar(a, b):
  ## from: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
  return SequenceMatcher(None, a, b).ratio()


def scrape_untappd(d, machine):

  out = []

  ## protection
  ua = UserAgent()
  rp = RotateProxies()


  for count, brewery in enumerate(d):
    header = ua.random
    proxy = rp.get_next()
    time.sleep(abs(throttle + np.random.normal(.5)))
    out.append(scrape_brewery(brewery, header, proxy))

    if count and not count % cache_frequency:
      cache(out, cache_dir, machine)
      out = []
      print('\n')
      print('################')
      print('Scraping brewery {} of {}'.format(count, len(d)))
      print('################')
      print('\n')

  return out

def scrape_brewery(brewery, header, proxy):

  url = 'https://untappd.com/search?q={}&type=brewery&sort='.format(urllib.parse.quote(brewery[1]))

  headers = {'User-Agent': header}
  print(proxy)
  page = []

  try:
    page = requests.get(url, headers = headers, proxies = proxy, timeout = 10)
  except:
    return {'brewery_id': brewery[0], 'data': None, 'request_code': 'Could not complete request'}

  if not page:
    return {'brewery_id': brewery[0], 'data': None, 'request_code': 'Could not complete request'}
  
  print('Brewery: {}, Status Code: {}'.format(brewery[1], page.status_code))

  if page.status_code != 200:
    return {'brewery_id': brewery[0], 'data': None, 'request_code': page.status_code}

  soup = BeautifulSoup(page.text, 'lxml')

  results = soup.select('div.results-container div.beer-item')

  match = get_match(results, brewery[1])

  if not match:
    return {'brewery_id': brewery[0], 'data': None, 'request_code': page.status_code}
  
  scraped_name = match.select('p.name')[0].text
  num_beers = int(match.select('p.abv')[0].text.strip().split()[0].replace(',', ''))
  num_ratings = int(match.select('p.ibu')[0].text.strip().split()[0].replace(',','')) 
  avg_rating = float(match.select('p.rating')[0].select('span.num')[0].text.replace('(','').replace(')', ''))


  out = {'brewery_id': brewery[0], 'request_status': page.status_code, 'data': {\
    'target_name': brewery[1],\
    'scraped_name': scraped_name,\
    'num_beers': num_beers, \
    'num_ratings': num_ratings, \
    'avg_rating':avg_rating}}

  print('Target name: {}, Scraped name: {}\n'.format(brewery[1], scraped_name))

  return out


def get_match(results_list, query_string):

  out = []

  for item in results_list:

    item_name = item.select('p.name')[0].text
    similarity = similar(query_string, item_name)
    out.append([item, similarity])

  out = sorted(out, key = lambda x: -x[1])

  if not out:
    return None

  return out[0][0]


def cache(d, cache_dir, machine):

  save_path = cache_dir + 'untappd_ratings_cache_{}.txt'.format(machine)

  if os.path.exists(save_path):
    prev = eval(open(save_path, 'r').read())
    d.extend(prev)

  file = open(save_path, 'w')
  file.write(str(d))
  file.close()



if __name__ == '__main__':

  args = sys.argv[1:]

  if len(args) != 2:
    print('Usage: breweries_names.txt machine')
    sys.exit(1)

  file = args[0]
  machine = args[1]


  d = eval(open(file, 'r').read())

  good_data = []

  if machine == 'desktop':
    d = d[:(len(d) // 2)]
  elif machine == 'laptop':
    d = d[(len(d) // 2):]
  

  if os.path.exists('../data/untappd/untappd_successful_scrapes_{}.txt'.format(machine)):
    good_data = eval(open('../data/untappd/untappd_successful_scrapes_{}.txt'.format(machine)).read())
    good_data_ids = [x['brewery_id'] for x in good_data]
    d = [x for x in d if x[0] not in good_data_ids]

  out = scrape_untappd(d, machine)

  if os.path.exists(cache_dir + 'untappd_ratings_cache_{}.txt'.format(machine)):
    prev = eval(open(cache_dir + 'untappd_ratings_cache_{}.txt'.format(machine), 'r').read())
    out.extend(prev)

  if good_data:
    out.extend([x for x in good_data if x['data']])

  file = open('../data/untappd/untappd_ratings_{}.txt'.format(machine), 'w')
  file.write(str(out))
  file.close()
