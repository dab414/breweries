from bs4 import BeautifulSoup
import requests

base = 'https://www.ewg.org/tapwater/search-results.php?zip5=18015&searchtype=zip'


page = requests.get(base)
soup = BeautifulSoup(page.text, 'lxml')

for tr in soup.find_all('tr'):
  td = tr.find('td')
  if td:
    result = td
    break

url = result.select('a')[0]['href']
name = result.select('a')[0].text

print(url, name)
