import requests
from bs4 import BeautifulSoup
import sys

class RotateProxies:

  def __init__(self):
    self.proxy_list = []


  def _generate_proxies(self):
    print('Resetting proxies . . .')
    print('\n')
    url = 'https://www.us-proxy.org/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    proxy_table = soup.select('table#proxylisttable tr')
    self.proxy_list = []

    for row in proxy_table[1:21]:
      if not row.select('td'):
        pass
      
      if row.select('td')[6].text == 'yes':
        http_code = 'https'
        ip = row.select('td')[0].text
        port = row.select('td')[1].text
        self.proxy_list.append({http_code: ip + ':' + port})
        
      else:
        pass
      
    return self

  def get_next(self):

    if not self.proxy_list:
      self._generate_proxies()

    validate = 1

    while validate:
      validate = self._validate_proxy()
      if validate:
        print('Bad connection: {}\n'.format(self.chosen_proxy))
      
    return self.chosen_proxy


  def _validate_proxy(self):
    if not self.proxy_list:
      self._generate_proxies()
    else:
      self.chosen_proxy = self.proxy_list.pop()
      try:
        page = requests.get('https://ifconfig.me/ip', proxies = self.chosen_proxy, timeout = 5)
      except:
        return 1
      
      if page.text == self.chosen_proxy['https'].split(':')[0] and page.status_code == 200:
        print('Successful connection: {}'.format(self.chosen_proxy))
        return 0

      return 1


      