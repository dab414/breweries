import requests
from bs4 import BeautifulSoup
import sys

def rate_beer_scrape(urls):
  ## takes in list of urls
  ## returns list of dicts with brewery data

  out = []

  for url in urls:
    out.append(page_scrape(url))

  return out


def page_scrape(url):
  ## takes in url
  ## returns dict with brewery data

  base = 'https://ratebeer.com'
  print(base + url)
  endpoint = base + url
  headers = ['Name', 'ABV', 'Added', '', 'Score', 'Style%', '#']

  page = requests.get(endpoint)

  soup = BeautifulSoup(page.text, 'lxml')

  beers ={}

  row_list = soup.select('table#brewer-beer-table tr')[1:]

  for row in row_list:
    col_list = row.select('td')
    for col, header in zip(col_list, headers):
      if len(col.select('a')) > 1:
        beers['Name'] = col.select('a')[0].text
        beers['Type'] = col.select('a')[1].text

      elif header:
        ## need to find a way to match the elements here with headers
        beers[header] = col.text.strip()

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

  print(out)

