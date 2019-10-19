import sys
import pandas as pd



def merge_data(centroids, water, demo):

  water = water.groupby('zipcode').count().reset_index()
  demo = demo[['zipcode', 'total', 'median_age']]

  centroids = centroids.set_index('zipcode').join(demo.set_index('zipcode')[['total', 'median_age']]).reset_index()
  centroids = centroids.set_index('zipcode').join(water.set_index('zipcode')['contam']).reset_index()
  centroids = centroids.rename(columns = {'total': 'total_population', 'contam': 'total_water_count'})


  return centroids



if __name__ == '__main__':

  args = sys.argv[1:]

  if not args:
    print('Usage: centroid_data.csv water_by_zip.csv demographics_by_zip.csv')
    sys.exit(1)

  centroids = pd.read_csv(args[0], dtype = {'zipcode': str})
  water = pd.read_csv(args[1], dtype = {'zipcode': str})
  demo = pd.read_csv(args[2], dtype = {'zipcode': str})

  out = merge_data(centroids, water, demo)

  out.to_csv('../data/centroid_data_with_summary.csv', index = False)