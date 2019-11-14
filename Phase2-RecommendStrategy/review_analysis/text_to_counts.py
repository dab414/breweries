import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys




def get_word_counts(d):

  text = d.dropna()['review_review_text'].values
  cv = CountVectorizer()
  cv.fit(text)
  out = []

  for word in cv.vocabulary_:
    out.append({'word': word, 'count': cv.vocabulary_[word]})

  return pd.DataFrame(out)




if __name__ == '__main__':

  args = sys.argv[1:]
  if not args:
    print('Usage: input_data.csv')
    sys.exit(1)

  path = args[0]

  d = pd.read_csv(path)
  
  get_word_counts(d).to_csv('dummy_word_counts.csv', index = False)