from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
print(this_directory)
with open(path.join(this_directory,'../README.md'), encoding='utf-8') as f:
      long_description = f.read()

setup(name='article_recommender',
      version='1.0.3',
      description='Create a recommendation engine for articles',
      packages=['article_recommender'],
      author='Celestin Hermez',
      author_email='celestinhermez@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)