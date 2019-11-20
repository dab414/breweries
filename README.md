# Building a Better Brewery
**Link to live app:** https://davebraun.org/beer

## Implementation

The goal of this project is to use data-driven insights to benefit both current and prospective brewery owners (see the **Business Objective** section below for more detail). The implementation of the app can broadly be divided into three phases: (1) defining competition areas, (2) matching a user zip code to a similar competition area, (3) analyzing a given competition area. The phases are described in more detail below, where you'll find links to some of the relevant scripts for each.

### Phase 1: Define Competition Regions

Defining brewery competition areas (i.e., regions) starts with the assumption that breweries are most directly in competition with other breweries in their physical proximity (think microbreweries and brew pubs). The approach was to get the longitude and latitude for all US microbreweries and brew pubs, cluser them based on latitude and longitude with K-Means, and use the latitude and longitude of the centroids to define the different competition areas. Below are a handful of scripts used to accomplish defining competition regions:  

* [`DefineCompetitionAreas.py`](Phase0-DefineCompetitionRegions/01-DefineCompetitionRegions/DefineCompetitionAreas.py): Takes in a CSV where each brewery is associated with its latitude / longitude. Returns A list of tuples where each tuple contains the latitude and longitude of centroids (i.e., competition area centers). Assigns each brewery to a competition area and saves out a labeled, brewery-level dataset.  
* [`ReverseGeocode.py`](Phase0-DefineCompetitionRegions/02-MatchCompetitionRegionsToZips/ReverseGeocode.py): Leverages an API from [Texas A&M](https://geoservices.tamu.edu/Services/ReverseGeocoding) to assign a zip code to each competition region.  
* [`extract_lat_lon.py`](Phase0-DefineCompetitionRegions/03-ParseUserZip/extract_lat_lon.py): Leverages a publicly available API ([opendatasoft](https://public.opendatasoft.com)) to return latitude / longitude when given a user's zip code.

### Phase 2: Find Similar Competition Regions

This phase involves collecting zip code data for each competition region, collecting the same data for the user's zip code, and matching the user's zip code to the most similar competition region. Better Brewery currently (11-19-2019) matches user zip codes to competition areas based on tap water data and demographic data. These scripts are the ones being executed in real time when a user enters a zip code.

**Scrape tap water data**  
* [`scrape_ewg.py`](Phase1-FindSimilarCompetitionRegions/water/scrape_ewg.py): This was a script that I found from [here](https://github.com/albertovilla/ewg/blob/master/EWG.ipynb) and modified it for my purposes. The goal was to scrape data about the types of contaminants in the tap water by zip code from [EWG Tap Water](https://www.ewg.org/tapwater/).  
* [`preprocess_water.py`](Phase1-FindSimilarCompetitionRegions/water/preprocess_water.py): The tap water data is initially saved in nested format. This preprocessing script converts the data such that each row is a new contaminant (matched with it's zip code). I.e., this script unnests the data.  

**Scrape demographic data**  
* [`census_scrape.py`](Phase1-FindSimilarCompetitionRegions/demographics/census_scrape.py): This script scrapes census data (e.g., age) from [Census.gov](https://factfinder.census.gov/faces/nav/jsf/pages/index.xhtml). The `webScrape()` function takes as input zipcode(s) and returns scraped census data, which allows it to be used for initially collecting data on the centroids or for parsing a user's zip code in real time. 

**Data aggregation / manipulation**  
* [`aggregate_data.py`](Phase1-FindSimilarCompetitionRegions/aggregate/aggregate_data.py): Takes the collected data for competition areas, joins data together, and converts data to wide format (i.e., dummy coding, one-hot encoding), so that the data is represented as one observation per competition area.  
* [`append_water_census_to_centroids.py`](Phase1-FindSimilarCompetitionRegions/manipulation_scripts/append_water_census_to_centroids.py): Computes summary statistics (i.e., tap water and demographics) for each competition area to be displayed in the info boxes when the user selects a competition area.  
* [`get_centroid_addresses.py`](Phase1-FindSimilarCompetitionRegions/manipulation_scripts/get_centroid_addresses.py): Leverages [Google's geocoding services](https://maps.googleapis.com/) to use zip codes in order to assign address information to the competition areas.
* [`process_incoming_zip.py`](Phase1-FindSimilarCompetitionRegions/processIncomingZip/process_incoming_zip.py): The main script used to handle scraping data in real time when given a zip code from the user.


### Phase 3: Recommend Strategy  

Once a user selects a competition area, the breweries in that competition area can be analyzed in order to recommend what a successful strategy might be in that competition area. Better Brewery currently (11-19-2019) presents a descriptive breakdown of top beers in the competition area. Deciding on a beer to brew is one of the first decisions that goes into opening a brewery, and this summary is meant to give users an easy place to start in terms of selecting a beer to brew. The next tab in the competition analyzer presents more data that the user can explore--the user is presented with a map of the competition area and is presented with brewery-level summary data after selecting a brewery on the map. The majority of this stage, thus far, has involved scraping the data to be used in the summaries. Below is a breakdown of the data sources, along with scripts used to execute data scraping.

* [`rate_beer_scrape.py`](Phase2-RecommendStrategy/ratebeer/rate_beer_scrape.py): [Ratebeer](https://www.ratebeer.com/) was the main data source for much of the data that currently drives Better Brewery. This script scrapes data on all breweries in the US from Ratebeer.  
* [`scrape_users.py`](Phase2-RecommendStrategy/twitter/scrape_users.py): Ratebeer lists the [Twitter](https://twitter.com) URL for each brewery. This script uses those URLs to scrape the Twitter account information for each brewery (if that brewery indeed had a Twitter account).  
**Untappd and Yelp**  
Scraping data from [Untappd](https://untappd.com) and [Yelp](https://yelp.com) was a bit more tricky because these sites work hard to prevent themselves from being scraped. Consequently, this scraping is still underway.  
* Untappd  
  * [`scrape_untappd.py`](Phase2-RecommendStrategy/untappd/scrape_untappd.py): The main script used to execute the scrape.  
  * [`rotate_proxies.py`](Phase2-RecommendStrategy/untappd/rotate_proxies.py): A class definition for rotating proxies for requests.  
* Yelp  
  These scripts were developed in very early iterations of the project and as such are somewhat messy...  
  * [`scrape_yelp.py`](Phase2-RecommendStrategy/yelp/scrapeYelp.py): The main script used to execute the scrape.  
  * [`protection.py`](Phase2-RecommendStrategy/yelp/protection.py): The main script used to manage rotating proxies.  

### Shiny App  
[R Shiny](https://shiny.rstudio.com/) was the framework in which the app was developed. The main scripts for running the app can be found in the following two directories:  
* [`ui`](ui/): Leveraging R's HTML API to develop the front end.  
* [`server`](server/): All files used to manage the backend data processing in the app.



## Business Objective

The business objective of Better Brewery is to provide a service for people who either own their own brewery or are looking to open their own brewery. Brewing beer has become increasingly popular over the last several decades, which means that there's a great deal of competition for those who are looking to get into the beer brewing business. My app is intended to make opening a brewery feel less overwhelming by giving prospective brewery owners an easy place to start.

The first step is to analyze the area that the user is looking to open a brewery and find other areas in the country that are similar in terms of their preconditions for brewery success. An example of what I mean by preconditions for success is something like tap water. Tap water is essential for brewing beer, and it's something about an area that cannot be changed. If I'm able to find areas that have similar tap water compared to our user's location, I can look to see how other breweries have been successful given that same tap water, and then make recommendations to the user about what strategies might be successful.

The current iteration of Better Brewery (11-13-2019) matches a user's location to similar location by analyzing tap water contaminants and demographic characteristcs. Once a user selects a similar region to analyze, the app simply presents the top rated beers in that competition area, as well as a review of the top rated beer. Choosing which beers to brew is often one of the first things that a new brewery owner needs to decide on. Presenting information on the top-performing beers is meant to give a user an easy place to start by suggesting which beers to brew first. The user can begin brewing these beers and trust that he or she is well on the way to building a better brewery.



Please don't hesitate to contact me with questions -> dab414@lehigh.edu

Best,
Dave

*-- I didn't upload some of the data, so the scripts won't be entirely reproducible if the repo is cloned--*



*Scripts for demoing*  

* [`get_similar_regions_from_zip.py`](get_similar_regions_from_zip.py)  
* [`process_incoming_zip.py`](Phase1-FindSimilarCompetitionRegions/processIncomingZip/process_incoming_zip.py)  
* [`find_closest.py`](Phase1-FindSimilarCompetitionRegions/findClosest/findClosest.py)

