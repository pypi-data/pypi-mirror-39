# poi_kml
This module defines classes and functions for converting a CSV file of points
of interest with addresses to a KML file for importing into mapping software.

# Installation
To install molib, use pip (or similar):
```{.sourceCode .bash}
pip install poi-kml
```

# Documentation

## First generate a test csv file
```python
fake_file = poi_kml.make_fake_poi_csv('sample_poi.csv', n=20)
```

## Example for generating a kml file
```python
db = poi_kml.POIdb(fake_file)
db.set_home('1200 E California Blvd, Pasadena, CA 91125')
db.filter(miles=25)
db.to_kml(filename='poi_near')
print(db.sort(by='Name'))
```