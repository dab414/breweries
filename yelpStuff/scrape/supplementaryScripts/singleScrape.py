
		#regString = r'{[^{]+\"addressLines\":\[\"201 41st St S\".*?]'
		## seems okay so far
		#regString = r'{\"rating[^{]*?\"addressLines\":\[\"201 41st St S\".*?]'
		regString = r'{\"rating[^{]*?\"addressLines\":\[\"2721 5th Ave S\".*?]'

		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

		#result = requests.get('https://www.yelp.com/search?find_desc=avondale+brewing&find_loc=birmingham', headers = headers, allow_redirects=False).text
		result = requests.get('https://www.yelp.com/search?find_desc=trim+tab+brewing&find_loc=birmingham', headers = headers, allow_redirects=False).text
		result = requests.get('https://www.yelp.com/search?find_desc=san+tan+brewing+co&find_loc=chandler', headers = headers, allow_redirects=False).text

		jsonPrep = re.search(regString, result).group()
		jsonData = json.loads(jsonPrep + '}')

		result = requests.get('https://www.yelp.com' + jsonData['businessUrl'], headers = headers, allow_redirects = False)

		tree = html.fromstring(result.content)

		raw_name = tree.xpath("//h1[contains(@class,'page-title')]//text()")
		raw_address = tree.xpath('//div[@class="mapbox-text"]//div[contains(@class,"map-box-address")]//text()')
		raw_moreInfo = tree.xpath('//h3[.="More business info"]/following::div[@class="short-def-list"]/*')
		raw_reviews = tree.xpath("//div[contains(@class,'biz-main-info')]//span[contains(@class,'review-count rating-qualifier')]//text()")[0].strip()
		raw_ratings = tree.xpath("//div[contains(@class,'biz-page-header')]//div[contains(@class,'rating')]/@title")

		## clean the raw entries
		rating = float(re.search('^\d+\.\d+', raw_ratings[0]).group())
		name = ''.join(raw_name).strip()
		address = ''.join(raw_address).strip()
		reviews = int(re.search('^\d+', raw_reviews).group())

		print raw_name, name

		moreInfo = []
		count = 0


		for e in raw_moreInfo:
			for j in e.itertext():
				if j.strip():
					if count == 0:
						build = j.strip()
						count = 1
					else:
						moreInfo.append([build, j.strip()])
						count = 0

		d = {
			'name': name,
			'address': address,
			'rating': rating,
			'reviews': reviews,
		}

		for entry in moreInfo:
			d[entry[0]] = entry[1]

		## we're gonna have a standardization problem down here
		## not all breweries have the same 'moreInfo'
		## as i see it now, the only ways to solve this are to either:
			## wide solution: store each attribute as a new feature, putting NA where features for breweries are missing
			## long solution: each brewery gets one row per added attribute

		## we'll eventually want a dataset where each brewery is summarized by one row... i think most MLs can't deal with long or missing data...

		print d		

