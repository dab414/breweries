import requests
import json
from lxml import html
import re
import urllib


def parseBreweryHtml(result, brewery):
  '''
  takes as input the html of the brewery page (result), and the dict for one brewery with keys [name, city, street]
  returns a list of dicts where each dict is the brewery and one of its 'moreInfo' attributes
  '''
  print 'Scraping specific page for: ' + brewery['name']
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


def parse(response, brewery):
  url = 'dummy'
  parser = html.fromstring(response)
  raw_name = parser.xpath("//h1[contains(@class,'page-title')]//text()")
  raw_claimed = parser.xpath("//span[contains(@class,'claim-status_icon--claimed')]/parent::div/text()")
  raw_reviews = parser.xpath("//div[contains(@class,'biz-main-info')]//span[contains(@class,'review-count rating-qualifier')]//text()")
  raw_category  = parser.xpath('//div[contains(@class,"biz-page-header")]//span[@class="category-str-list"]//a/text()')
  hours_table = parser.xpath("//table[contains(@class,'hours-table')]//tr")
  raw_moreInfo = parser.xpath('//h3[.="More business info"]/following::div[@class="short-def-list"]/*')
  raw_map_link = parser.xpath("//a[@class='biz-map-directions']/img/@src")
  raw_phone = parser.xpath(".//span[@class='biz-phone']//text()")
  raw_address = parser.xpath('//div[@class="mapbox-text"]//div[contains(@class,"map-box-address")]//text()')
  raw_wbsite_link = parser.xpath("//span[contains(@class,'biz-website')]/a/@href")
  raw_price_range = parser.xpath("//dd[contains(@class,'price-description')]//text()")
  raw_health_rating = parser.xpath("//dd[contains(@class,'health-score-description')]//text()")
  rating_histogram = parser.xpath("//table[contains(@class,'histogram')]//tr[contains(@class,'histogram_row')]")
  raw_ratings = parser.xpath("//div[contains(@class,'biz-page-header')]//div[contains(@class,'rating')]/@title")

  working_hours = []
  for hours in hours_table:
    raw_day = hours.xpath(".//th//text()")
    raw_timing = hours.xpath("./td//text()")
    day = ''.join(raw_day).strip()
    timing = ''.join(raw_timing).strip()
    working_hours.append({day:timing})

  '''
  info = []
  for details in details_table:
    raw_description_key = details.xpath('.//dt//text()')
    raw_description_value = details.xpath('.//dd//text()')
    description_key = ''.join(raw_description_key).strip()
    description_value = ''.join(raw_description_value).strip()
    info.append({description_key:description_value})
  '''

  ratings_histogram = [] 
  for ratings in rating_histogram:
    raw_rating_key = ratings.xpath(".//th//text()")
    raw_rating_value = ratings.xpath(".//td[@class='histogram_count']//text()")
    rating_key = ''.join(raw_rating_key).strip()
    rating_value = ''.join(raw_rating_value).strip()
    ratings_histogram.append({rating_key:rating_value})
  
  name = ''.join(raw_name).strip()
  phone = ''.join(raw_phone).strip()
  address = ' '.join(' '.join(raw_address).split())
  health_rating = ''.join(raw_health_rating).strip()
  price_range = ''.join(raw_price_range).strip()
  claimed_status = ''.join(raw_claimed).strip()
  reviews = ''.join(raw_reviews).strip()
  category = ','.join(raw_category)
  cleaned_ratings = ''.join(raw_ratings).strip()

  if raw_wbsite_link:
    decoded_raw_website_link = urllib.unquote(raw_wbsite_link[0])
    website = re.findall("biz_redir\?url=(.*)&website_link",decoded_raw_website_link)[0]
  else:
    website = ''
  
  if raw_map_link:
    decoded_map_url =  urllib.unquote(raw_map_link[0])
    map_coordinates = re.findall("center=([+-]?\d+.\d+,[+-]?\d+\.\d+)",decoded_map_url)[0].split(',')
    latitude = map_coordinates[0]
    longitude = map_coordinates[1]
  else:
    latitude = ''
    longitude = ''

  if raw_ratings:
    ratings = re.findall("\d+[.,]?\d+",cleaned_ratings)[0]
  else:
    ratings = 0

  moreInfo = parseMoreInfo(raw_moreInfo)

  breweryList = []
  
  for entry in moreInfo:
    data={
      'name': brewery['name'],
      'city': brewery['city'],
      'street': brewery['street'],      
      'ratings':ratings,
      'health_rating':health_rating,
      'price_range':price_range,
      'claimed_status':claimed_status,
      'reviews':reviews,
      'category':category,
      'moreInfoVar': entry[0],
      'moreInfoVal': entry[1],
    }

    ## add ratings histogram
    for e in ratings_histogram:
      data[str(e.keys()[0][0]) + '_star_count'] = e[e.keys()[0]]

    ## add working hours
    for e in working_hours:
      data[e.keys()[0][:3]] = e[e.keys()[0]]

    breweryList.append(data)


  return breweryList


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