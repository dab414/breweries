#!/home/dave/anaconda2/bin/python
import unicodedata
import requests
import json
import re
from lxml import html
import pandas as pd
import numpy as np
import urllib
import difflib
from fake_useragent import UserAgent
import time
import sys
sys.path.insert(0, 'protection/')
from protection import *
from parseBreweryHtml import *

startingPoint = 2400
endingPoint = 3000

## dict for interpreting health of proxies
healthCode = {
  0: 'Excellent',
  1: 'Pretty Good',
  2: 'Fair',
  3: 'Unwell',
  4: 'On the Verge of Death',
  5: 'Dead'
}

### SEARCHING FUNCTIONS ###

def generateNullBrewery(brewery):
  brewery['reviews'] = 'NA'
  brewery['rating'] = 'NA'
  brewery['moreInfoVar'] = 'NA'
  brewery['moreInfoVal'] = 'NA'
  return brewery


def searchHtmlToBusinessUrl(result, brewery):
  '''
  takes as input the html of the search page, and the dict with brewery keys [name, city, street]
  returns the businessUrl for only the brewery of interest
  '''

  regString = r'searchResultBusiness":({.*?title.*?}]})'

  ## attempt to regex search results by address
  try:
    jsonPrep = re.findall(regString, result)
  except:
    print '\n'
    print 'RexExing the search results failed'
    print 'Strike against the proxy'
    print '\n'
    ## report the error
    return ['', 1]

  ## gives to the function all regex matches in the search page
  ## returns a list of dicts where each dict is a non-ad seach result
  ## also returns a dict where {'breweryName': its rank on the search page}
  [searchResults, breweryNames] = parseSearchHtml(jsonPrep)

  ## function goes through list of search result dicts and returns the one whose business name most closely matches the query name
  return findMatchingBrewery(searchResults, breweryNames, brewery)

def parseSearchHtml(jsonPrep):
  '''
  takes as input the text results of the regex of the search page
  returns a list of dicts where each dict is a non-ad seach result
  also returns a dict where {'breweryName': its rank on the search page}
  '''
  breweryNames = {}
  searchResults = []
  numResult = 0

  try:
    for e in jsonPrep:
        jsonBrewery = json.loads(e)
        if not jsonBrewery['isAd']:
            searchResults.append(jsonBrewery)
            breweryNames[jsonBrewery['name']] = numResult
            numResult += 1
  except Exception as err:
    print 'Parsing the search HTML threw an error'
    print str(err)
    d = {'name':0, 'name':0}
    searchResults = [d,d]

  return [searchResults, breweryNames]

def findMatchingBrewery(searchResults, breweryNames, brewery):
  '''
  takes as input: 
      searchResults: a list of dicts where each dict is a non-ad seach result
      breweryNames: a dict where {'breweryName': its rank on the search page}
  returns the businessUrl of the matching brewery
  '''
  try:
    print 'critical brewery name: ' + brewery['name']
    print '----------'
    print 'brewery search keys: ' + str(breweryNames.keys())
    candidates = difflib.get_close_matches(brewery['name'], breweryNames.keys(), cutoff = .7)
    if candidates:
      for e in searchResults:
          if e['name'] == candidates[0]:
              print 'Scraping the specific page of: ' + e['name']
              return [e['businessUrl'], 0]
    else:
      ## if search result sets are continually null it suggests that yelp is blocking the ip
      print 'Failed to find a matching brewery.'
      return ['', 1]

  except Exception as err:
    print 'something went wrong when trying to find a matching brewery'
    print 'aborting this brewery'
    return ['', 1] 


### SUMMARIZING FUNCTIONS ###

def summarizeBreweries(breweries):
  '''
  takes as input list of dicts where each dict is {'name': name, 'city': city, 'street': street}
  returns as output list of dicts where each dict contains scraped attributes of the brewery
  '''

  ## initialize the empty result list
  output = []

  ## list for holding blocked proxies
  blackList = []

  ## generate first proxy set
  proxySet = findFwcProxies('', blackList)

  ## start new iterator
  proxyIterator = iter(proxySet)

  ## initialize header generator
  ua = UserAgent()

  ## list to store breweries for which searches fail
  searchFails = []

  ## iterate over breweries
  ## each brewery scrape will be executed by a different proxy
  for count, brewery in enumerate(breweries):
    print '\n'

  ## generate headers
    headers = {'User-Agent': ua.random}

    ## select a proxy
    status = 1
    while status:

      catch = 0
      try:
        currentProxy = next(proxyIterator)
        status = testProxy(constructProxyDict(currentProxy))

      ## if we've ran through all the proxies in the set
      except:
        proxySummary(proxySet, healthCode)
        print 'Generating new proxy set.'
        print '\n'
        try:
          proxySet = findFwcProxies(proxySet, blackList)
          proxyIterator = iter(proxySet)
          currentProxy = next(proxyIterator)
          status = testProxy(constructProxyDict(currentProxy))
        except:
          print 'Something went wrong while trying to access sslproxies.org'
          catch = 1
      
      ## prune proxies that don't work
      if status and not catch:
        proxySet.remove(currentProxy)

    print 'Active proxy: ' + str(currentProxy)
    print '\n'

    ## turn the full proxy dict into a small dict for the requests call
    proxies = constructProxyDict(currentProxy)

    errCode = 0
    ## search request
    [result, errCode] = makeRequest(brewery, headers, proxies)

    
    if not errCode:
	    ## returns the businessUrl
      try:
        [businessUrl, errCode] = searchHtmlToBusinessUrl(result, brewery)
      except Exception as err:
        print 'Something went wrong that didnt get handled properly in the searchHtmlToBusinessUrl() procedure'
        errCode = 1 
	    
    ## if search failed, append nulls to output and abort loop
    if errCode:
      ## update the search fails dict
      searchFails.append(brewery)
      output.append(generateNullBrewery(brewery))
      [proxySet, blackList] = updateProxies(1, currentProxy, proxySet, blackList)
      
      if (count + 1) % 100 == 0:
        saveCache(count, output, searchFails)
        print 'Failed Searches: ' + str(pd.DataFrame(searchFails)[['name','city','street']])

      continue

    
    try:

      ## throw a timeout
      time.sleep(np.max([np.random.normal(2,1,1), 0.5]))

      ## scrape html of brewery specific page on yelp
      [result, status] = makeRequest(businessUrl, headers, proxies)

      ## add to output (as a flat list) the list of dicts for each brewery, where each dict has one of that brewery's attributes
      output += parse(result, brewery)

      ## report that the proxy was successful
      [proxySet, blackList] = updateProxies(0, currentProxy, proxySet, blackList)

    except:
      print 'Something went wrong scraping the specific page of the brewery. Counting it as a strike against the proxy.'
      [proxySet, blackList] = updateProxies(1, currentProxy, proxySet, blackList)
      ## update the search fails dict
      searchFails.append(brewery)
      

    print '\n'
    ## RESTART FLAG
    print 'I just parsed brewery ' + str(breweries.index(brewery) + 1) + ' of ' + str(len(breweries)) + ' breweries.'
    print '--------------'

    ## save out cache
    if (count + 1) % 100 == 0:
      saveCache(count, output, searchFails)
      print 'Failed Searches: ' + str(pd.DataFrame(searchFails)[['name','city','street']])

    print output
  
  proxySummary(proxySet, healthCode)
  return [output, searchFails]



def saveCache(count, output, searchFails):
  ## RESTART FLAG
  try:
    df = pd.DataFrame(output)
    print 'Saving out a copy of the data at cache point ' + str(count + startingPoint + 1) + '.'
    df.to_csv('cache/yelpData' + str(startingPoint) + '-' + str(count + startingPoint + 1) + '.csv', index = False)

    df = pd.DataFrame(searchFails)[['name', 'city', 'street']]
    df.to_csv('cache/searchFails' + str(startingPoint) + '-' + str(count + startingPoint + 1) + '.csv', index = False)

    
  except Exception as err:
    print 'Trying to save a copy of the data at cache point ' + str(count  + startingPoint + 1) + ' caused an error.'
    print str(err)

### MAIN ###

def main():
  ## read in brewery data and save out important columns as np arrays
  ## url encode where needed
  brew = pd.read_csv('../data/breweries.csv')

  ## drop breweries with duplicate names
  brew = brew.drop_duplicates(subset = 'name')

  ## RESTART FLAG
  brew = brew.iloc[startingPoint:endingPoint]

  ## save only the variables of interest and convert to a list of dicts
  breweries = brew[['name', 'city', 'street']].to_dict('records')

  ## execute scraping
  [output, searchFails] = summarizeBreweries(breweries)

  ## pass lists of brewery information to function and get in return list of dicts where each dict contains features for each brewery
  try:
    with open('exportData/listOfDicts.txt', 'w') as fout:
      json.dump(output, fout)
  except Exception as err:
    print 'Trying to save the list of dicts to file threw an error'
    print str(err)

  ## convert result to data frame and save
  try:
    pd.DataFrame(output).to_csv('exportData/yelpData' + str(startingPoint) + '-' + str(endingPoint) + '.csv', index = False)
    pd.DataFrame(searchFails)[['name','city','street']].to_csv('exportData/searchFails' + str(startingPoint) + '-' + str(endingPoint) + '.csv', index = False)
  except Exception as err:
    print 'Trying to convert and save the list of dicts to a dataframe threw an error'
    print str(err)

if __name__ == '__main__':
  main()