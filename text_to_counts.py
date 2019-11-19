import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys




def get_word_counts(d):
  ## takes in df where one of the columns is 'review_review_text'
  print('Input:')
  print(d)
  text = pd.DataFrame(d, columns = ['brewery_id', 'review_review_text']).dropna()['review_review_text'].values
  cv = CountVectorizer(stop_words = 'english')
  
  try:
    cv_fit = cv.fit_transform(text)
  except ValueError as e:
    if 'empty vocabulary' in str(e):
      return 'Not enough reviews to make a wordcloud. Try selecting a different brewery.'
    else:
      return 'An unknown problem occurred. Try selecting a different brewery.'


  counts = cv_fit.toarray().sum(axis = 0)

  out = []

  for word, count in zip(cv.get_feature_names(), counts):
    out.append({'word': word, 'count': count})



  #return pd.DataFrame(out)
  return pd.DataFrame(out)

'''


if __name__ == '__main__':

  args = sys.argv[1:]
  if not args:
    print('Usage: input_data.csv')
    sys.exit(1)

  path = args[0]

  d = pd.read_csv(path)
  
  print(get_word_counts(d))

'''