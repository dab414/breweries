import sys

## assumes that the script is being run in its own directory


if __name__ == '__main__':
  args = sys.argv[1:]

  if not args:
    print('Usage: All the raw ratebeer files you want to convert to twitter data')
    sys.exit(1)

  out = []

  for count, arg in enumerate(args):
    d = eval(open(arg, 'r').read())
    out.extend([(x['brewery_id'], x['twitter_link']) for x in d])
    print('finished: {}'.format(count + 1))
    del d

  f = open('../data/twitter/breweries_twitter_links.txt', 'w')
  f.write(str(out))
  f.close()