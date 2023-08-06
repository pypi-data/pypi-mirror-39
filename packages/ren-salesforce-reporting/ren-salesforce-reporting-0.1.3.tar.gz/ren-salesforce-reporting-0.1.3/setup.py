from setuptools import setup

setup(
  name = 'ren-salesforce-reporting',
  packages = ['ren_salesforce_reporting'],
  version = '0.1.3',
  description = 'Get data from Salesforce reports with python',
  author = 'Ren Ku',
  author_email = 'raikoo31@gmail.com',
  url = 'https://github.com/renyuku/salesforce-reporting',
  keywords = ['python', 'salesforce', 'salesforce.com'],
  install_requires= ['requests'],
  classifiers = [
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3'
  ],
  include_package_data=True,
)
