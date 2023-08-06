# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poi_kml']

package_data = \
{'': ['*']}

install_requires = \
['faker>=1.0,<2.0',
 'geocoder>=1.38,<2.0',
 'pandas>=0.23.4,<0.24.0',
 'pathlib>=1.0,<2.0',
 'phonenumbers>=8.10,<9.0',
 'simplekml>=1.3,<2.0',
 'usaddress>=0.5.10,<0.6.0',
 'uszipcode>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'poi-kml',
    'version': '0.1.0',
    'description': '',
    'long_description': "# poi_kml\nThis module defines classes and functions for converting a CSV file of points\nof interest with addresses to a KML file for importing into mapping software.\n\n# Installation\nTo install molib, use pip (or similar):\n```{.sourceCode .bash}\npip install poi_kml\n```\n\n# Documentation\n\n## First generate a test csv file\n```python\nimport fake_poi_list_generator as fakepoi\nfake_file = fakepoi.make_fake_poi_csv('sample_poi.csv', n=20)\n```\n\n## Example for generating a kml file\n```python\ndb = POIdb(fake_file)\ndb.set_home('1200 E California Blvd, Pasadena, CA 91125')\ndb.filter(miles=25)\ndb.to_kml(filename='poi_near')\nprint(db.sort(by='Name'))\n```",
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
