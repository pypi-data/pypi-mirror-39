from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='cob_arcgis_geocoder',
      version='0.0.2',
      description='Python geocoder to be used in ETL pipelines',
      url='https://github.com/CityOfBoston/cob_arcgis_geocoder',
      author='Analytics Team',
      author_email='analytics@boston.gov',
      packages=['cob_arcgis_geocoder'],
zip_safe=False)
