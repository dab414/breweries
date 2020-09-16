import sys
import requests
import pandas as pd

sys.path.append('../../private')
from census_api_key import *

## not entirely necessary because we can assume the vars will come in in this order
data_key = {
	
	'B01001_002E': 'count_male',
	'B01001_026E': 'count_female',
	'B00001_001E': 'total',
	'B02001_002E': 'white',
	'B02001_003E': 'black',
	'B02001_005E': 'asian',
	'B02001_004E': 'native',
	'B02001_008E': 'two_plus',
	'B03002_001E': 'hispanic',
	#'non_hispanic': 'no',
	'B01002_001E': 'median_age',
	'B01001_003E': 'male_under_five',
	'B01001_005E': 'male_ten_fourteen',
	'B01001_006E': 'male_fifteen_twentyfour',
	'B01001_011E': 'male_twentyfive_fortyfour',
	'B01001_015E': 'male_fortyfive_fiftynine',
	'B01001_018E': 'male_sixty_seventyfour',
	'B01001_027E': 'female_under_five',
	'B01001_029E': 'female_ten_fourteen',
	'B01001_030E': 'female_fifteen_twentyfour',
	'B01001_035E': 'female_twentyfive_fortyfour',
	'B01001_039E': 'female_fortyfive_fiftynine',
	'B01001_042E': 'female_sixty_seventyfour'

}

url_stem = 'https://api.census.gov/data/2018/acs/acs5'
get_args = '?get='
for_args = r'&for=zip%20code%20tabulation%20area:'
variable_names = ','.join(list(data_key.keys()))
key = '&key={}'.format(api_key)


def compile_zipcode_data(zipcode_list):
	data, headers = zipcode_iterator(zipcode_list)
	return data_aggregator(data, headers)



def zipcode_iterator(zipcode_list):
	# takes in zipcodes as a list

	headers = list(data_key.values())
	headers.append('zipcode')
	data = []

	for zipcode in zipcode_list:
		data.append(call_census_api(zipcode))

	return data, headers


def call_census_api(zipcode):
	#returns a list of data corresponding to the input zipcode

	url = url_stem + get_args + variable_names + for_args + zipcode + key
	result = requests.get(url_stem + get_args + variable_names + for_args + zipcode + key)
	
	return result.json()[1]
	


def data_aggregator(data, headers):
	## takes in data as a list of lists and headers as a list
	## returns consolidated data as a df
	
	## convert all but zipcode to integer
	zipcode = data[0].pop(-1)
	data = [int(float(e)) for e in data[0]]
	data.append(zipcode)
	d = pd.DataFrame([data], columns = headers)

	

	## create summary columns
	d['non_hispanic'] = d['total'] - d['hispanic'] 
	d['under_five'] = d['male_under_five'] + d['female_under_five']
	d['ten_fourteen'] = d['male_ten_fourteen'] + d['female_ten_fourteen']
	d['fifteen_twentyfour'] = d['male_fifteen_twentyfour'] + d['female_fifteen_twentyfour']
	d['twentyfive_fortyfour'] = d['male_twentyfive_fortyfour'] + d['female_twentyfive_fortyfour']
	d['fortyfive_fiftynine'] = d['male_fortyfive_fiftynine'] + d['female_fortyfive_fiftynine']
	d['sixty_seventyfour'] = d['male_sixty_seventyfour'] + d['female_sixty_seventyfour']

	## drop unnecessary columns
	d.drop(['male_under_five','female_under_five', 'male_ten_fourteen', 'female_ten_fourteen', 'male_fifteen_twentyfour', 'female_fifteen_twentyfour', 'male_twentyfive_fortyfour', 'female_twentyfive_fortyfour', \
		'male_fortyfive_fiftynine', 'female_fortyfive_fiftynine', 'male_sixty_seventyfour', 'female_sixty_seventyfour'], axis = 1)

	## reorder
	headers_ordered = ['zipcode', 'count_male', 'count_female', 'total', 'white', 'black', 'asian', 'native', 'two_plus', 'hispanic', 'non_hispanic',\
    'median_age', 'under_five', 'ten_fourteen', 'fifteen_twentyfour', 'twentyfive_fortyfour', 'fortyfive_fiftynine', 'sixty_seventyfour']

	d = d[headers_ordered]

	return d
	

if __name__ == '__main__':

	args = sys.argv[1:]

	if not args:
		print("Usage: zipcode")
		sys.exit(1)

	zipcode = str(args[0])

	out = compile_zipcode_data([zipcode])