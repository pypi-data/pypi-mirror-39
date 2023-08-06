# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
	try:
	    with open('README.rst') as f:
	        return f.read()
	except:
		pass

setup(name = 'gnfetcher',
      version = '1.0.0',
      classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
	    'Programming Language :: Python :: 2',
	    'Programming Language :: Python :: 2.6',
	    'Programming Language :: Python :: 2.7',
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 3.3',
	    'Programming Language :: Python :: 3.4',
	    'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
      ],
      keywords = 'google news feed python tool',
      scripts = ['bin/gnews-gui'], 
      description = 'Python client for Google News feed.',
      long_description = readme(),
      url = 'http://github.com/aadu999/gnfetcher',
      author = 'Adarsh Raveendra',
      author_email = 'hello@adarsh.online',
      license = 'MIT',
      packages = ['gnfetcher', 'gnfetcher.scripts'],
      install_requires = ['requests', 'bs4', 'html5lib', 'Click'], 
      include_package_data = True,
      zip_safe = False,
      entry_points='''
        [console_scripts]
        gnews=gnfetcher.scripts.gnews:cli
      ''',
      )
