import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
import numpy as np
import pickle
import os
import time


def findFwcProxies(prevProxies, blackList):
  '''
  takes nothing as input
  returns list of dicts where each dict is a profile of a crawler from a first-world country with keys ['id', 'ip', 'port', 'country', 'health']
  '''
  ua = UserAgent()
  proxies = []  
  count = 0

  ## open text list of first world countries
  try:
    f = open('protection/firstWorldCountries.txt', 'r')
    fwc = [e.strip() for e in f]
  except:
    print 'Unable to open the text file containing first world countries. Aborting'
    sys.exit()

  ## scrape sslproxies.org 
  headers = {'User-Agent': ua.random}
  result = requests.get('https://sslproxies.org/', headers = headers)

  ## parse html
  soup = BeautifulSoup(result.text, 'lxml')
  proxies_table = soup.find(id = 'proxylisttable')


  ## build up list of dicts for all proxies
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip': row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string,
      'country': row.find_all('td')[3].string,
      })

  ## keep only those proxies from first world countries
  proxies = [e for e in proxies if e['country'] in fwc]

  ## initialize id and health information
  for number, crawler in enumerate(proxies):
    crawler['health'] = 0
    crawler['recentAttempts'] = ['na' for i in range(5)]


  ## if there were previous proxies
  if prevProxies:
    
    oldIps = []
    oldIds = []
    
    ## grab the ids and ips from them
    for proxy in prevProxies:
        oldIps.append(proxy[1]['ip'])
        oldIds.append(proxy[0])

    ## grab IPs from the blackList
    for proxy in blackList:
      oldIps.append(proxy[1]['ip'])

    # find the max ip to use for numbering the ids of new proxies
    maxId = np.array(oldIds).max()

    ## number the new proxies starting at 1 + the max of the old id
    for count, proxy in enumerate(proxies):
      proxies[count] = (maxId + 1, proxy)
      maxId += 1

    ## determine whether new proxies are unique and should be added to old proxies
    for proxy in proxies:
      if proxy[1]['ip'] not in oldIps:
        prevProxies.append(proxy)

    return prevProxies

  ## if there are no previous proxies
  else:
    
    ## label their ids 0:length 
    for number, proxy in enumerate(proxies):
      proxies[number] = (number, proxy)

    #saveProxies(proxies)

    return proxies


def updateProxies(code, currentProxy, proxySet, blackList):
  '''
  takes as input currentProxy and its failure/success code [0, 1]
  ONE MEANS FAIL
  also takes in the proxySet and blackList
  reutrns updated proxySet and blackList
  '''

  relevantAttempts = currentProxy[1]['recentAttempts']

  ## go through existing entries and walk them back
  for attempt in range(1, 5):
    relevantAttempts[attempt - 1] = relevantAttempts[attempt]

  ## update 5th entry with the code
  relevantAttempts[4] = code

  ## if it's not still one of the first few runs for the proxy
  if 'na' not in relevantAttempts:

    ## BLACK LIST CATCHER
    ## if the proxy has struck out five times in a row, kill it
    if np.array(relevantAttempts).sum() == 5:
      proxySet.remove(currentProxy)
      currentProxy[1]['recentAttempts'] = relevantAttempts
      currentProxy[1]['health'] = 5
      blackList.append(currentProxy)
      print 'Proxy: ' + str(currentProxy) + ' has just died.'
      print '\n'
      print str(len(proxySet)) + ' total proxies are still alive.'

    ## othewise, record the new code, update the health, and exit
    else:
      for number, proxy in enumerate(proxySet):
        if proxy[0] == currentProxy[0]:
          proxySet[number][1]['health'] = np.array(relevantAttempts).sum()
          proxySet[number][1]['recentAttempts'] = relevantAttempts

  ## if it is still one of the first few runs for the proxy
  else:
    ## just throw the updated attempts back on the list and exit
    for number, proxy in enumerate(proxySet):
      if proxy[0] == currentProxy[0]:
        proxySet[number][1]['recentAttempts'] = relevantAttempts

  return [proxySet, blackList]


def testProxy(proxy):
  '''
  takes as input proxies dict
  returns 0 if proxy successfully connects to a server, 1 otherwise
  logic of function from: https://stackoverflow.com/questions/492519/timeout-on-a-function-call
  '''  
  import signal
  status = 1

  def handler(signum, frame):
    print 'Proxy timed out'
    print '\n'
    raise Exception()

  def attemptRequest(proxy):
    return requests.get('http://www.ipconfig.me/ip', proxies = proxy).text

  signal.signal(signal.SIGALRM, handler)

  signal.alarm(5)

  try:
    result = attemptRequest(proxy)
    if result == proxy['http'].split(':')[0]:
      status = 0

  except:
    print 'Proxy ' + str(proxy) + ' is no good'
    print '\n'

  signal.alarm(0)

  return status



def makeRequest(params, headers, proxies):
  '''
  takes as input proxies dict
  returns 0 if proxy successfully connects to a server, 1 otherwise
  logic of function from: https://stackoverflow.com/questions/492519/timeout-on-a-function-call
  '''  
  import signal
  import urllib
  status = 1

  def handler(signum, frame):
    print 'Proxy timed out on Yelp request (10s)'
    print '\n'
    raise Exception()

  def attemptRequest(params, headers, proxies):
    if len(params) == 3:
      ## IM REMOVING THE LOCATION DESCRIPTION ON THE SEARCH PARAMETER
      ## i think it's too restricting
      return requests.get('https://www.yelp.com/search?find_desc=' + urllib.quote_plus(params['name']) + \
        r'&find_loc=' + urllib.quote_plus(params['name']), headers = headers, proxies = proxies, allow_redirects=False).text
    else:
       return requests.get('https://www.yelp.com' + params, headers = headers, allow_redirects = False).text

  signal.signal(signal.SIGALRM, handler)

  signal.alarm(10)

  try:
    result = attemptRequest(params, headers, proxies)
    status = 0

  except Exception as err:
    print 'Request failed for ' + str(params['name'])
    print str(err)
    result = ''
    print '\n'

  signal.alarm(0)
  return [result, status]



def proxySummary(proxySet, healthCode):
  print "We've run through all the proxies, here is a summary of the health of the remaining ones:"
  print '\n'
  for proxy in proxySet:
    if 'na' not in proxy[1]['recentAttempts']:
      print 'Proxy ID: ' + str(proxy[0]) + ', Proxy Health: ' + healthCode[proxy[1]['health']]
      print '\n'
    else:
      print 'Proxy ID: ' + str(proxy[0]) + ', Proxy Attempts: ' + str(proxy[1]['recentAttempts'])

  print '\n'


def constructProxyDict(currentProxy):
  out = {
    'http': currentProxy[1]['ip'] + ':' + currentProxy[1]['port'],
    'https': currentProxy[1]['ip'] + ':' + currentProxy[1]['port']
  }

  return out


