# https://www.openbrewerydb.org/

import requests
import json
import pandas as pd

## there are only 161 pages if you show 50 results per page
pageRange = range(1,162)

df = pd.DataFrame(json.loads(requests.get('https://api.openbrewerydb.org/breweries?page=1&per_page=50').text))
count = 1

for page in pageRange:
	result = requests.get('https://api.openbrewerydb.org/breweries?page=' + str(page) + '&per_page=50').text
	if result:
		try:
			df = df.append(json.loads(result))
		except:
			count += 1
			df.to_csv('breweries'+str(count)+'.csv', index = False, encoding = 'utf-8', header = True)
			df = pd.DataFrame(json.loads(result))
			print('Page: ' + str(page) + ' failed to append. Starting new dataframe.')
	print(page)

print(df.shape)
count += 1
df.to_csv('breweries'+str(count)+'.csv', index = False, encoding = 'utf-8', header = True)