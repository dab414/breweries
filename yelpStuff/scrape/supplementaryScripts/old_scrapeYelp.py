import unicodedata
import requests
import json
import re
from lxml import html
import pandas as pd
import numpy as np
import urllib
from creepyCrawlers import superSpider
import difflib

def parseMoreInfo(raw_moreInfo):
	'''
	takes as input the strange xpath object and returns a list of list where each list is [category, value]
	'''

	moreInfo = []
	count = 0

	## iterate over the weird xpath object
	for e in raw_moreInfo:
		for j in e.itertext():
			## end up getting lines of text separated by lots of blank lines
			## if we hit a line that has text on it
			if j.strip():
				## the first line will always be the key
				if count == 0:
					build = j.strip()
					count = 1
				## the next line will always be the value
				else:
					moreInfo.append([build, j.strip()])
					count = 0

	return moreInfo


def performYelpSearch(regString, result, brewery):
	'''
	takes as input the regex search string, the html of the search page, and the dict with brewery keys [name, city, street]
	returns the html search result for only the brewery of interest
	'''
	print brewery['street']

	## attempt to regex search results by address
	try:
		jsonPrep = re.search(regString, result).group()
		return [jsonPrep, 0]
	except Exception as err:
		ErrorMessage = str(err)
		print 'Failed to RegEx the address of ' + brewery['name'] + ' in search results.'
		print 'Calling in the Super Spider'
		[jsonPrep, errCode] = superSpider(regString, result, brewery)

		## this area won't work because i never finished superSpider()

		if errCode:
			print 'The Super Spider has failed'
			brewery['rating'] = 'NA'
			brewery['reviews'] = 'NA'
			brewery['moreInfoVar'] = 'NA'
			brewery['moreInfoVal'] = 'NA'
			return ['', brewery]
		else:
			print 'The Super Spider has succeeded'
			return [jsonPrep, 0]

def parseBreweryHtml(result, brewery):
	'''
	takes as input the html of the brewery page (result), and the dict for one brewery with keys [name, city, street]
	returns a list of dicts where each dict is the brewery and one of its 'moreInfo' attributes
	'''
	print brewery['name']
	## create a tree object that can be navigated with xpath
	tree = html.fromstring(result.content)

	## perform xpath searches
	## i think i got this code from elsewhere but don't remember where
	## something similar to this: https://gist.github.com/scrapehero/d8cf3d8b7039b8ba3dcde9b607cdc7de
	raw_name = tree.xpath("//h1[contains(@class,'page-title')]//text()")
	raw_address = tree.xpath('//div[@class="mapbox-text"]//div[contains(@class,"map-box-address")]//text()')
	raw_moreInfo = tree.xpath('//h3[.="More business info"]/following::div[@class="short-def-list"]/*')
	raw_reviews = tree.xpath("//div[contains(@class,'biz-main-info')]//span[contains(@class,'review-count rating-qualifier')]//text()")
	raw_reviews = tree.xpath("//div[contains(@class,'biz-main-info')]//span[contains(@class,'review-count rating-qualifier')]//text()")[0].strip()
	raw_ratings = tree.xpath("//div[contains(@class,'biz-page-header')]//div[contains(@class,'rating')]/@title")

	## clean the raw entries
	try:
		rating = float(re.search('^\d+\.\d+', raw_ratings[0]).group())
	except:
		rating = 'NA'
	name = ''.join(raw_name).strip()
	address = ''.join(raw_address).strip()
	try:
		reviews = int(re.search('^\d+', raw_reviews).group())
	except:
		reviews = 'NA'

	## returning a list of lists where each list is [category, value]
	moreInfo = parseMoreInfo(raw_moreInfo)

	breweryList = []

	for entry in moreInfo:
		data = {
			'name': brewery['name'],
			'city': brewery['city'],
			'street': brewery['street'],
			'reviews': reviews,
			'rating': rating,
			'moreInfoVar': entry[0],
			'moreInfoVal': entry[1]
		}
		breweryList.append(data)


	return breweryList


def summarizeBreweries(breweries):
	'''
	takes as input list of dicts where each dict is {'name': name, 'city': city, 'street': street}
	returns as output list of dicts where each dict contains scraped attributes of the brewery
	'''

	## define browser headers
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

	## initialize the empty result list
	output = []

	## iterate over breweries
	for brewery in breweries:

		#define regex string
		regString = r'{\"rating[^{]*?\"addressLines\":\[\"' + brewery['street'] + r'\".*?]'

		## make initial search request
		result = requests.get('https://www.yelp.com/search?find_desc=' + urllib.quote_plus(brewery['name']) + \
			r'&find_loc=' + urllib.quote_plus(brewery['name']), headers = headers, allow_redirects=False).text
		
		## perform search
		[jsonPrep, errCode] = performYelpSearch(regString, result, brewery)
		
		## if search failed, append nulls to output and abort loop
		if errCode:
			output.append(errCode)
			continue

		## convert brewery search entry to a dict
		jsonData = json.loads(jsonPrep + '}')

		## scrape html of brewery specific page on yelp
		result = requests.get('https://www.yelp.com' + jsonData['businessUrl'], headers = headers, allow_redirects = False)

		## add to output (as a flat list) the list of dicts for each brewery, where each dict has one of that brewery's attributes
		output += parseBreweryHtml(result, brewery)

	return output




def main():
	## read in brewery data and save out important columns as np arrays
	## url encode where needed
	brew = pd.read_csv('../data/breweries.csv')

	## FOR DEVELOPMENT
	brew = brew[:10]

	## save only the variables of interest and convert to a list of dicts
	breweries = brew[['name', 'city', 'street']].to_dict('records')

	## execute scraping
	output = summarizeBreweries(breweries)

	## pass lists of brewery information to function and get in return list of dicts where each dict contains features for each brewery
	try:
		with open('exportData/listOfDicts.txt', 'w') as fout:
			json.dump(output, fout)
	except Exception as err:
		print 'Trying to save the list of dicts to file threw an error'
		print str(err)

	## convert result to data frame and save
	try:
		pd.DataFrame(output).to_csv('exportData/yelpData.csv', index = False)
	except Exception as err:
		print 'Trying to convert and save the list of dicts to a dataframe threw an error'
		print str(err)

if __name__ == '__main__':
	main()