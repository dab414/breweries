# Building a Better Brewery
## Looking at brewery data to benefit both consumers and owners

The goal of this project is to use data-driven insights to benefit both brewery owners and consumers. Below are links to some of the important aspects of the project thus far.  

* Scraping Scripts  
  * A list of about 8,000 breweries was obtained from [openbrewerydb.org](https://openbrewerydb.org). The following scripts successfully scraped about 2,400 of these breweries from Yelp on their first attempt.  
  * [`scrapeOpenBrewery.py`](data/scrapeOpenBrewery.py): The script used to scrape breweries from [openbrewerydb.org](https://openbrewerydb.org)
  * [`scrapeYelp.py`](yelpStuff/scrape/scrapeYelp.py): The main script used to execute the scrape.  
  * [`parseBreweryHtml.py`](yelpStuff/scrape/parseBreweryHtml.py): Scraping the brewery-specific pages on Yelp.  
  * [`protection.py`](yelpStuff/scrape/protection/protection.py): Managing and rotating proxies for Yelp requests.

* Data Analysis  
  * [Data Cleaning](https://htmlpreview.github.io/?https://github.com/dab414/breweries/blob/master/yelpStuff/analysis/scripts/dataCleaning.html): Cleaning and organizing the raw Yelp data.
  * [Exploratory Data Analysis](https://htmlpreview.github.io/?https://github.com/dab414/breweries/blob/master/yelpStuff/analysis/scripts/yelpEDA.html): Initial insights from the data.  



Please don't hesitate to contact me with questions -> dab414@lehigh.edu

Best,
Dave

*-- I didn't upload some of the data, so the scripts won't be entirely reproducible if the repo is cloned--*

[Notes](yelpStuff/scrape/protection/notes.txt): A little taste of how I think about things and stuff.