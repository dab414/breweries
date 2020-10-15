from math import sqrt
import sys
import pandas as pd
import requests

def compute_distance(user_loc, centroid_list):
	## user loc is [lat, lon]
	## centroid list is [(label, [lat, lon]), (label, [lat, lon]), ...]
	## return nearest cluster label

	closest_centroid = None

	for centroid in centroid_list:
		label = centroid[0]
		centroid_loc = centroid[1]

		distance = sqrt((user_loc[0] - centroid_loc[0])**2 + (user_loc[1] - user_loc[1])**2)

		if closest_centroid is None or distance < closest_centroid[1]:
			closest_centroid = (label, distance)
		
	return closest_centroid[0]


def find_closest_to_user(lat, lon, centroids):

	## takes in lat and lon associated with user zip code
	## all i really need to return is the label associated with the nearest competition area

	centroids = centroids[['label', 'latitude', 'longitude']]

	centroids = [(int(x[0]), [x[1], x[2]]) for x in centroids.values]

	return compute_distance([lat, lon], centroids)




def extract_lat_lon(user_zip):

  base = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&facet=state&facet=timezone&facet=dst&q='

  data = eval(requests.get(base + user_zip).text)


  if data['nhits']:
    return data['records'][0]['fields']

  return 'ZIPCODE INVALID'


if __name__ == '__main__':


	zipcode = sys.argv[1]
	result = extract_lat_lon(zipcode)
	centroids = pd.read_csv('../data/aggregated_data.csv')

	print(find_closest_to_user(result['latitude'], result['longitude'], centroids))