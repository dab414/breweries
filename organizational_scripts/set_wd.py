import os


def set_wd():
  
  root = '/home/dave/OneDrive/Professional Development/Fellowships/incubator/capstoneProject/'

  if 'dave' not in os.getcwd():
    root = '/'

  return root