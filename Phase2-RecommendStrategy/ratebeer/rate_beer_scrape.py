import requests
from bs4 import BeautifulSoup
import sys
import re

base = 'https://ratebeer.com'

def rate_beer_scrape(urls):
  ## takes in list of urls
  ## returns list of dicts with brewery data

  out = []

  for url in urls:

    ## PUT TIMEOUT HERE

    out.append(page_scrape(url))

  return out


def page_scrape(url):
  ## takes in url
  ## returns dict with brewery data

  print(base + url)
  endpoint = base + url
  

  page = requests.get(endpoint)

  soup = BeautifulSoup(page.text, 'lxml')

  out = {}

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


  out['reviews'] = extract_reviews(page)

  out['beers'] = extract_beers(soup)

  return out



def extract_reviews(page):
  ## returns a list of dicts where each dict is one review of one beer

  review_data = []

  # get brewer id
  brewer_id = re.search(r'BrewerID=(\d+)', page.text).group(1)

  reviews_page = requests.get(base + '/ajax/brewer-recent.asp?bid={}'.format(brewer_id))

  review_soup = BeautifulSoup(reviews_page.text, 'lxml')

  review_list = review_soup.select('div.row div.bubbleleft')

  for row in review_list:
    review = {}

    review['beer_name'] = row.select('strong')[0].text
    review['beer_score'] = row.select('div.score')[0].text
    review['review_date'] = row.select('small')[0].text
    review['review_text'] = row.select('span')[0].text

    review_data.append(review)

  return review_data



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





if __name__ == '__main__':

  args = sys.argv[1:]

  '''
  if args != 1:
    print('Usage: list_of_urls.txt')
    sys.exit(1)

  urls = args
  '''

  # dev
  urls = ['/brewers/avondale-brewing-company/12890/']

  out = rate_beer_scrape(urls)

  f = open('test.txt', 'w')
  f.write(str(out[0]))
  f.close()

