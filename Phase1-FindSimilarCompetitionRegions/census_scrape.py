import requests
import re
import numpy as np
import pandas as pd
import sys

'''
this script automatically takes in the data in `../data/input.csv`
returns `../data/output.csv` with demographic data for each input zip code
where there is no data in the system for a given zip, these entries are marked with `-99999`
'''

def clean_codes(raw_codes):
	'''
	takes as input csv containing zips in first column and checks to make sure they're all five digit strings
	returns list of string zip codes
	'''
	x = np.array(raw_codes['zip'])
	x = x.astype(str)
	x = x[[len(i) == 5 for i in x]]
	return x.tolist()

def webScrape(inputCsv):

	x = pd.read_csv(inputCsv)
	zipcodes = clean_codes(x)

	base = 'https://factfinder.census.gov/'
	report = base + 'bkmk/table/1.0/en/ACS/16_5YR/DP05/8600000US'
	geoCheck = base + 'rest/communityFactsNav/nav?N=0&searchTerm='
	render = base + 'tablerestful/tableServices/renderProductData'

	final_data = []

	with requests.session() as s:
		s.headers['user-agent'] = 'Mozilla/5.0'

		for count, zipcode in enumerate(zipcodes):
			c = s.get(geoCheck + zipcode)

			## handling zipcodes where there is no data available
			if c.json()['CFMetaData']['isNotValidGeo'] or c.json()['CFMetaData']['displayNoDataAvailableMsg']:
				total = white = black = asian = native = two_plus = -999999

			else:
				s.get(report + zipcode)
				r = s.get(render)
				try:
					html = r.json()['ProductData']['productDataTable']
				except:
					print zipcode
					sys.exit()

				total = int(re.search('r30.*Total population.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
				white = int(re.search('r34.*White.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
				black = int(re.search('r35.*Black or African American.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
				asian = int(re.search('r41.*Asian.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
				native = int(re.search('r49.*Native Hawaiian and Other Pacific Islander.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
				two_plus = int(re.search('r32.*Two or more races.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))

			final_data.append([zipcode, total, white, black, asian, native, two_plus])
			
			## progress tracker
			if count in [178, 350, 534]:
				print 'Progress: Iteration ' + str(count) + ' of ' + str(len(zipcodes))


	out_data = pd.DataFrame(final_data, columns = ['zipcode', 'total', 'white', 'black', 'asian', 'native', 'two_plus'])

def main():
	args = sys.argv[1:]

	if not args or len(args) > 1:
		print 'Usage: file.csv'
		sys.exit()

	out_data = webScrape(args)
	out_data.to_csv('output.csv')

if __name__ == '__main__':
	main()
