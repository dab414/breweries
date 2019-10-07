import requests
import re
import numpy as np
import pandas as pd
import sys

'''
this script takes in a txt file where the contents are a list of string zipcodes 
returns `../data/demographics_by_zip.csv` with demographic data for each input zip code
where there is no data in the system for a given zip, these entries are marked with `-99999`
'''

def clean_codes(raw_codes):
  '''
  takes as input csv containing zips in first column and checks to make sure they're all five digit strings
  returns list of string zip codes
  '''
  x = np.array(raw_codes)
  x = x.astype(str)
  x = x[[len(i) == 5 for i in x]]
  return x.tolist()

def webScrape(inputCsv):

  #x = pd.read_csv(inputCsv)
  x = eval(open(inputCsv, 'r').read())
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
      if c.json()['CFMetaData'].get('isNotValidGeo') or c.json()['CFMetaData'].get('displayNoDataAvailableMsg'):
        male = female = total = white = black = asian = native = two_plus = -999999

      else:
        s.get(report + zipcode)
        r = s.get(render)
        try:
          html = r.json()['ProductData']['productDataTable']
        except:
          print(zipcode)
          sys.exit()

        male = int(re.search(r'r3.*Male.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        female = int(re.search(r'r4.*Female.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        median_age = float(re.search(r'r18.*Median age.*?>(\d.*?)<\/td>', html).group(1))
        total = int(re.search(r'r30.*Total population.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        white = int(re.search(r'r34.*White.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        black = int(re.search(r'r35.*Black or African American.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        asian = int(re.search(r'r41.*Asian.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        native = int(re.search(r'r49.*Native Hawaiian and Other Pacific Islander.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        two_plus = int(re.search(r'r32.*Two or more races.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        hispanic = int(re.search(r'r70.*Hispanic or Latino.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))
        non_hispanic = int(re.search(r'r75.*Not Hispanic or Latino.*?>(\d.*?)<\/td>', html).group(1).replace(',',''))

      final_data.append([zipcode, male, female, median_age, total, white, black, asian, native, two_plus, hispanic, non_hispanic])
      
      ## progress tracker
      if len(zipcodes) > 100:
        if not count % (len(zipcodes) // 10):
          print('Progress: Iteration ' + str(count) + ' of ' + str(len(zipcodes)))


  out_data = pd.DataFrame(final_data, columns = ['zipcode', 'count_male', 'count_female', 'median_age', 'total', 'white', 'black', 'asian', 'native', 'two_plus', 'hispanic', 'non_hispanic'])

  return out_data

def main():
  args = sys.argv[1:]

  if not args or len(args) > 1:
    print('Usage: file.txt')
    sys.exit()

  out_data = webScrape(args[0])
  out_data.to_csv('../data/demographics_by_zip.csv', index = False)

if __name__ == '__main__':
  main()
