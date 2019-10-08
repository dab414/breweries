import sys
import numpy as np
import pandas as pd
import math


def compute_similarity(new_obs, centroids):

  new_obs, centroids = normalize_count(new_obs, centroids)

  new_obs = convert_to_array(new_obs)
  centroids_arr = convert_to_array(centroids)

  similar_centroids = find_distances(new_obs, centroids_arr)

  return centroids[[x[0] for x in similar_centroids]]


def find_distances(new_obs, centroids):

  obs_features = new_obs[0][1]

  distances = []

  for index, centroid in enumerate(centroids):
    sse = 0
    for obs_feature, base_feature in zip(obs_features, centroid[1]):
      sse += (base_feature - obs_feature)**2

    distances.append((index, math.sqrt(sse)))

  distances = sorted(distances, key = lambda x: x[1])


  return distances[:3]


def normalize_count(new_obs, centroids):

  ## combine all data
  d = pd.concat([new_obs, centroids])

  ## take out cols that arent counts
  zips_labels = d[['zipcode', 'label']]
  d = d.drop(['zipcode', 'label'], axis = 1)

  ## normalize
  d = d.apply(lambda x: x / x.sum())

  ## put cols back in 
  d = pd.concat([zips_labels, d], axis = 1)

  ## split data back apart
  new_obs = d.iloc[-1]
  centroids = d.drop(d.tail(1).index)


  return new_obs, centroids





def convert_to_array(d):
  ## ISSUE AROUND HERE
  print(d[['zipcode', 'label']].values)
  zips_labels = [tuple(x) for x in d[['zipcode', 'label']].values]
  features = [tuple(x) for x in d.drop(['zipcode', 'label'], axis = 1).values]

  out = []

  for name, features in zip(zips_labels, features):
    out.append((name, (features)))

  return out
  




if __name__ == '__main__':
  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: aggregated_data.csv')
    sys.exit(1)

  d = pd.read_csv(args[0], dtype = {'zipcode': str})

  new_obs = d.sample()
  centroids = d.drop(new_obs.index)

  print(compute_similarity(new_obs, centroids))