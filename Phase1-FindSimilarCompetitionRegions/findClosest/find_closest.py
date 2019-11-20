import sys
import numpy as np
import pandas as pd
import math


def compute_similarity(new_obs, centroids):
  ## first function called

  centroids = centroids.drop('median_age', axis = 1)

  new_obs, centroids = normalize_count(new_obs, centroids)

  new_obs = convert_to_array(new_obs)
  centroids_arr = convert_to_array(centroids)

  similar_centroids = find_distances(new_obs, centroids_arr)

  crit_labels = [x[0] for x in similar_centroids]

  return centroids[centroids['label'].isin(crit_labels)][['zipcode', 'label', 'longitude', 'latitude']]


def find_distances(new_obs, centroids):
  ## returns list of three best matching competition areas as: [('label', )]

  obs_features = new_obs[0][1]

  distances = []

  ## calculate euclidean distance
  for centroid in centroids:
    sse = 0
    for obs_feature, base_feature in zip(obs_features, centroid[1]):
      sse += (base_feature - obs_feature)**2

    distances.append((centroid[0][1], math.sqrt(sse)))

  distances = sorted(distances, key = lambda x: x[1])


  return distances[:3]


def normalize_count(new_obs, centroids):

  new_obs_zip = new_obs['zipcode'].values[0]

  ## combine all data
  ## save out centroid labels
  centroid_labels = centroids[['zipcode', 'label']]

  d = pd.concat([new_obs, centroids.drop('label', axis = 1)], sort = True)

  ## take out cols that arent counts
  zips_labels = d[['zipcode', 'latitude', 'longitude']]  
  d = d.drop(['zipcode', 'latitude', 'longitude'], axis = 1)

  ## normalize
  d = d.apply(lambda x: x / x.sum())

  ## put cols back in 
  d = pd.concat([zips_labels, d], axis = 1)

  ## split data back apart
  new_obs = d[d['zipcode'] == new_obs_zip]
  centroids = d[d['zipcode'] != new_obs_zip]

  ## put labels back in centroid data
  centroids = pd.concat([centroids, centroid_labels['label']], axis = 1, sort = True)
  
  return new_obs, centroids





def convert_to_array(d):
  ## need two separate cases depending on whether incoming data is new_obs or base_data
  
  out = []

  if d.shape[0] > 1:
    zips_labels = [tuple(x) for x in d[['zipcode', 'label', 'latitude', 'longitude']].values]
    features = [tuple(x) for x in d.drop(['zipcode', 'label', 'latitude', 'longitude'], axis = 1).values]

    for name, features in zip(zips_labels, features):
      out.append((name, (features)))

  else:
    zips_labels = d[['zipcode', 'latitude', 'longitude']].values[0]
    features = d.drop(['zipcode', 'latitude', 'longitude'], axis = 1).values[0]
    out.append((zips_labels, (features)))

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