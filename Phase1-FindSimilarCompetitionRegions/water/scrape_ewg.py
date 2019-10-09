## from https://github.com/albertovilla/ewg/blob/master/EWG.ipynb

import pandas as pd
import progressbar
import pprint
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.ewg.org/tapwater/'
SEARCH_URL_START = 'search-results.php?zip5='
SEARCH_URL_END = '&searchtype=zip'


def got_results_from_url(soup, url):
    error = soup.find('h2', text = 'No systems found that match your search')
    if (error):
        return False
    else:
        return True

def generate_url_from_zip(zip_value):
    return BASE_URL + SEARCH_URL_START + zip_value + SEARCH_URL_END

def get_population(people_served_tag):
    return int(people_served_tag.replace('Population served:', '').replace(',',''))

def get_city(element):
    return element.text.split(',')[0].strip()

def extract_info_from_row(elements):
    row_info = {}
    row_info['url'] = BASE_URL + elements[0].find('a')['href']
    row_info['utility_name'] = elements[0].text
    row_info['city'] = get_city(elements[1])
    row_info['people_served'] = get_population(elements[2].text)
    return row_info

def process_results(results, zip_value, state_id):
    zip_results = []
    result_rows = results.find_all('tr')
    for row in result_rows:
        elements = row.find_all('td')
        if elements:
            element = extract_info_from_row(elements)
            element['zip'] = zip_value
            element['state'] = state_id
            zip_results.append(element)
    return zip_results

def process_zip(zip_value, state_id):
    url = generate_url_from_zip(zip_value)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    if got_results_from_url(soup, url):
        results = soup.find_all('table', {'class': 'search-results-table'})
        # NOTE: there are two search-results-table, first one shows the results for the 
        # largest utilities serving County, the second one is more complete and includes
        # utilities serving the searched zip and the surrounding county
        # The process will be applied only to the LARGEST UTILITIES which is the first 
        # result
        return process_results(results[0], zip_value, state_id)
    else:
        return []
    
def get_contaminants(soup, contaminant_type):
    section = soup.find('ul', {'class': 'contaminants-list', 'id': contaminant_type})
    if section:
        contaminants_type = section.find_all('div', {'class': 'contaminant-name'})
        contaminants = []
        for contaminant in contaminants_type:
            contaminant_name = contaminant.find('h3').text
            if len(contaminant_name) < 80:
                contaminants.append(contaminant.find('h3').text)
        return contaminants
    else:
        return []
    
def get_contaminants_above_hbl(soup):
    return get_contaminants(soup, 'contams_above_hbl')

def get_contaminants_other(soup):
    return get_contaminants(soup, 'contams_other')  

def get_all_contaminants(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    contaminants_above_hbl = get_contaminants_above_hbl(soup)
    contaminants_other = get_contaminants_other(soup)
    
    return (contaminants_above_hbl, contaminants_other)
    
def scrap_contaminants_from_df(df):
    contaminants_rows = []
   
    status = 0
    bar = progressbar.ProgressBar(maxval=df.shape[0])
    bar.start()
    
    for index, utility in df.iterrows():
        # percentage of completion
        bar.update(status)        
        status = status + 1
        
        r = requests.get(utility['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        
        row = {}
        row['zip'] = utility['zip']
        row['city'] = utility['city']        
        row['contaminants_above_hbl'] = get_contaminants_above_hbl(soup)
        row['contaminants_other'] = get_contaminants_other(soup)
        contaminants_rows.append(row)
    bar.finish()
    
    return contaminants_rows
    
def scrape_ewg(df):
    data = []
       
    status = 0
    bar = progressbar.ProgressBar(maxval=df.shape[0])
    bar.start()
    
    # Step 1: get information about the utilities in each zip code    
    for index, row in df.iterrows():
        # percentage of completion
        bar.update(status)        
        status = status + 1
        
        utilities = process_zip(row['zip'], row['state_id'])
        data = data + utilities
    bar.finish()
    
    # Let's save this to a CSV just in case the second process does not work
    utilities_df = pd.DataFrame(data)
    utilities_df.to_csv('utilities.csv', index=False)
        
    # Step 2: for each utility obtain the contaminants
    status = 0
    bar = progressbar.ProgressBar(maxval=len(data))
    bar.start()

    for utility in data:
        # percentage of completion
        bar.update(status)        
        status = status + 1
        
        r = requests.get(utility['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        utility['contaminants_above_hbl'] = get_contaminants_above_hbl(soup)
        utility['contaminants_other'] = get_contaminants_other(soup)
    bar.finish()
    
    return data



if __name__ == '__main__':
  df = pd.read_csv('../data/centroid_data.csv')
  df = df.rename(columns = {'Zip': 'zipcode', 'State': 'state_id'})

  result = scrape_ewg(df[['zip', 'state_id']].dropna())

  pd.DataFrame(result).to_csv('../data/water_by_zip_raw.csv', index = False)