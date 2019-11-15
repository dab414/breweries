## OBJECTIVE
  ## take in brewery dataset
  ## return list of tuples where each tuple contains lat / lon of a competition area centroid

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import sys

## constants
## defined relative to next dir up
data_path = '../Phase2-RecommendStrategy/data/brewery_features_df.csv'
usa_box = [-125.771484, 23.725012, -66.269531, 49.239121]
usa_lat = [usa_box[1], usa_box[3]]
usa_lon = [usa_box[0], usa_box[2]]


def import_extract():

  d = pd.read_csv(data_path)
  d = d[['brewery_id', 'latitude', 'longitude']]
  lat_filter = (d['latitude'] > usa_lat[0]) & (d['latitude'] < usa_lat[1])
  lon_filter = (d['longitude'] > usa_lon[0]) & (d['longitude'] < usa_lon[1])
  d = d[(lat_filter & lon_filter)]
  
  return d



def run_clustering(d, n_clusters = 150):

  km = KMeans(n_clusters = n_clusters, random_state = 55).fit(d)

  return km.cluster_centers_, km.labels_


def prune_small_clusters(centroids, d, min_brew = 5):
  ## it looks like one can assume that the cluster label corresponds to 
  ## the index of km.cluster_centers unless the algorithm doesn't converge... ?

  original_cluster_count = len(centroids)

  ## aggregate and only keep clusters with counts greater than or equal to min_brew
  keep = d.groupby('label').count().reset_index()
  keep = keep[keep['brewery_id'] >= min_brew]

  centroids = pd.DataFrame(centroids)
  centroids['label'] = centroids.index
  centroids = centroids[centroids['label'].isin(keep['label'])]
  d = d[d['label'].isin(keep['label'])]

  print('Number of clusters pruned: {}'.format(original_cluster_count - len(centroids)))

  return centroids, d




def main():
  d = import_extract()
  centroids, d['label'] = run_clustering(d[['latitude', 'longitude']])
  centroids, d = prune_small_clusters(centroids, d)

  d.to_csv('../Phase2-RecommendStrategy/data/brewery_features_df_labeled.csv', index = False)
  #d.to_csv('temp_breweries.csv', index = False)
  
  return centroids



if __name__ == '__main__':
  out = main()
  out.to_csv('temp_centroids.csv', index = False)