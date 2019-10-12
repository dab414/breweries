import requests
from bs4 import BeautifulSoup
import sys
import re
import time
import numpy as np
from fake_useragent import UserAgent
import os

base = 'https://ratebeer.com'
user_agent = 'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.2.20) Gecko/20110803 Firefox/3.6.20'
first_request_timeout = 2.5
second_request_timeout = 2

def rate_beer_scrape(urls, machine_id):
  ## takes in list of urls
  ## returns list of dicts with brewery data

  out = []
  bad_brews = []

  ua = UserAgent()

  for count, url in enumerate(urls):

    ## PUT TIMEOUT HERE
    time.sleep(first_request_timeout + np.random.normal(0, .4))

    header = ua.random

    result, code = page_scrape(url, header, '{}_{}'.format(machine_id, count))

    if code:
      bad_brews.append(result)
      
    else:
      out.append(result)

    if count and not count % 100:
      print('\n')
      print('#####################')
      print('Processing brewery {} of {}.\n'.format(count, len(urls)))
      print('#####################')
      print('\n')
      cache(out, machine_id)
      out = []

  return out, bad_brews


def page_scrape(url, header, brewery_id):
  ## takes in url
  ## returns dict with brewery data

  print(base + url)
  endpoint = base + url
  
  headers = {'User-Agent': header}
  page = requests.get(endpoint, headers = headers)

  if page.status_code != 200:
    print('BAD FIRST REQUEST: Code = {}, URL = {}'.format(page.status_code, url))
    print('\n')
    return {'url': url, 'code': page.status_code}, 1

  soup = BeautifulSoup(page.text, 'lxml')

  out = {}

  ## get name
  out['brewery_name'] = soup.select('h1', {'itemprop': 'name'})[0].text

  out['brewery_id'] = brewery_id

  ## brewery type
  out['brewery_type'] = soup.select('h1', {'itemprop': 'name'})[0].parent.find_next_sibling('div').text.strip()

  ## request code
  out['request_status'] = page.status_code

  ## get address
  out['address'] = soup.select('span a', {'itemprop': 'address'})[0].text.strip() 

  ## get twitter data
  for e in soup.select('div.media-links a'):
    if 'twitter' in e['href']:
      out['twitter_link'] = e['href']

  ## if the brewery has no twitter link
  if 'twitter_link' not in out:
    out['twitter_link'] = None

  review_result, code = extract_reviews(page, headers, url)

  if code:
    out['reviews'] = None

  else:
    out['reviews'] = review_result

  out['beers'] = extract_beers(soup)


  return out, 0



def extract_reviews(page, headers, url):
  ## returns a list of dicts where each dict is one review of one beer

  review_data = []

  # get brewer id
  brewer_id = re.search(r'BrewerID=(\d+)', page.text).group(1)

  time.sleep(second_request_timeout + np.random.normal(0, .5))
  reviews_url = base + '/ajax/brewer-recent.asp?bid={}'.format(brewer_id)
  reviews_page = requests.get(reviews_url , headers=headers)

  if reviews_page.status_code != 200:
    print('BAD SECOND REQUEST: Code = {}, URL1 = {}, URL2 = {}'.format(reviews_page.status_code, url, reviews_url))
    print('\n')
    return reviews_page.status_code, 1

  review_soup = BeautifulSoup(reviews_page.text, 'lxml')

  review_list = review_soup.select('div.row div.bubbleleft')

  for row in review_list:
    review = {}

    review['beer_name'] = row.select('strong')[0].text
    review['beer_score'] = row.select('div.score')[0].text
    review['review_date'] = row.select('small')[0].text
    review['review_text'] = row.select('span')[0].text

    review_data.append(review)

  return review_data, 0



def extract_beers(soup):

  beers = []

  row_list = soup.select('table#brewer-beer-table tr')[1:]

  headers = ['beer_name', 'ABV', 'beer_date_added', '', 'beer_score', 'beer_style_percentile', 'num_reviewers']

  for row in row_list:
    beer = {}
    col_list = row.select('td')
    for col, header in zip(col_list, headers):
      if len(col.select('a')) > 1:
        beer['Name'] = col.select('a')[0].text
        beer['Type'] = col.select('a')[1].text

      elif header:
        ## need to find a way to match the elements here with headers
        beer[header] = col.text.strip()

      beers.append(beer)

  return beers


def cache(out, machine_id):
 
  filepath = '../data/cache/ratebeer_cache_{}.txt'.format(machine_id)

  if os.path.exists(filepath):
    prev = eval(open(filepath, 'r').read())
    
  else:
    prev = []

  f = open(filepath, 'w')
  f.write(str(prev.extend(out)))
  f.close()
    


if __name__ == '__main__':

  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: [laptop, desktop]')
    sys.exit(1)

  machine_id = args[0]

  ## im just gonna hard code gabe's data

  d = eval(open('ratebeer_data_from_gabe.txt', 'r').read())
  
  urls = []

  for state in d:
    urls.extend(state['list_of_breweries'])

  out, bad_brews = rate_beer_scrape(urls[750:870], machine_id)

  if os.path.exists('../data/cache/ratebeer_cache.txt'):
    prev = eval(open('../data/cache/ratebeer_cache_{}.txt'.format(machine_id), 'r').read())
    out.extend(prev)

  f = open('../data/ratebeer_{}.txt'.format(machine_id), 'w')
  f.write(str(out))
  f.close()

  f = open('../data/ratebeer_bad_brews_{}.txt'.format(machine_id, 'w'))
  f.write(str(bad_brews))
  f.close()

