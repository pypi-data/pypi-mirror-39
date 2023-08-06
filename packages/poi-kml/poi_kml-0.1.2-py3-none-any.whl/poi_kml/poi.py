#-----------------------------------------------------------------------------#
# Manny Ochoa -- 17 November 2018 -- Ver. 1.0.0 -- initial revision
#-----------------------------------------------------------------------------#
'''
Point of Interest list to KML (poi.py)

This module defines classes and functions for converting a CSV file of points
of interest with addresses to a KML file for importing into mapping software.
To test it, use fake_poi_list_generator.py to generate a sample dataset.
'''

#-----------------------------------------------------------------------------#
# LIBRARIES
#-----------------------------------------------------------------------------#
from pathlib import Path
import pandas as pd
import simplekml
import uszipcode
import geocoder

#----------------------------------------------------------------------------#
# CLASSES AND FUNCTIONS
#----------------------------------------------------------------------------#
class POIdb(object):
	''' Filters a list of points of interest based on distance from a street
		address (using an OpenStreetMaps API) and/or by state. Creates a kml
		file for uploading to Google maps. Expects a csv database with at
		least the following columns (in any order):
			Name,Address,State,Zip,Phone,Latitude,Longitude
	'''

	# CLASS CONSTANTS
	ERR_MSG_NO_ADDRESS = 'Please set reference address with set_home().'
	DEFAULT_KML_FILENAME = 'poi_list'


	def __init__(self, filename, home=None):
		self.file = Path(filename)
		self.home = home
		self.df_orig = pd.read_csv(self.file)
		self.validate_df(self.df_orig)
		self.df = self.df_orig.copy()

	def __len__(self):
		return len(self.df)

	def __str__(self):
		print(self.df)
		return ''

	def validate_df(self, df):
		header = 'Name,Address,State,Zip,Phone,Latitude,Longitude'.split(',')
		if not all(k in df for k in header):
			raise MissingDataColumns(MissingDataColumns.msg)

	def fill_states_and_zip(self, df):
		'''Updates Zip and State if not in df, given FullAddress.
		Might take a while, due to multiple calls to OpenStreetMaps.'''
		records = []
		for id,row in df.iterrows():
			g = geocoder.osm(row['FullAddress'])
			records.append((g.state, g.postal))
		df['Zip'] = [Zip for (Zip,State) in records]
		df['State'] = [Zip for (Zip,State) in records]
		return self

	def _update_home_coords(self):
		g = geocoder.osm(self.home)
		self.lat, self.lng = g.latlng
		self.zip = g.postal
		self.state = g.state
		return self

	def set_home(self, address):
		self.home = address
		self._update_home_coords()
		return self

	def reload(self):
		self.df = self.df_orig.copy()
		return self

	def sort(self, **kwargs):
		'''Sorts the data (Pandas df) in place'''
		self.df.sort_values(**kwargs, inplace=True)
		return self

	def filter(self, states=None, miles=None, reload=True):
		if reload:
			self.reload() # start with complete initial dataset before filtering
		if states:
			state_set = states.upper().split()
			self.df = self.df[self.df.State.isin(state_set)]
		if miles:
			if self.home is None: # check for address
				raise AssertionError(self.ERR_MSG_NO_ADDRESS)
			self._update_home_coords() # update coordinates
			zip_data = uszipcode.SearchEngine().by_coordinates(
				lat=self.lat,
				lng=self.lng,
				radius=miles,
				returns=None)
			valid_zip_codes = set([record.zipcode for record in zip_data]
								+ [self.zip]) # always include home zip code
			self.df = self.df[self.df.Zip.isin(valid_zip_codes)]
		return self

	def to_kml(self,filename=None):
		kml=simplekml.Kml()
		for id,row in self.df.iterrows():
			kml.newpoint(
				name=row['Name'],
				description=str(row['Address']) + '\n' + str(row['Phone']),
				coords=[(float(row['Longitude']), float(row['Latitude']))])
		output_filename = filename if filename else self.DEFAULT_KML_FILENAME
		output_dir = Path('.', 'output')
		output_dir.mkdir(parents=True, exist_ok=True)
		kml.save(output_dir/(output_filename + '.kml'))
		print('Created file ' + str(Path(output_filename + '.kml')))
		return self


class MissingDataColumns(Exception):
	'''Raised when the data is missing columns from the expected ones.'''
	msg = 'Please use a csv database with at least the following columns\n\
		  (in any order): Name,Address,State,Zip,Phone,Latitude,Longitude'
	pass

#----------------------------------------------------------------------------#
# SAMPLE SCRIPT
#----------------------------------------------------------------------------#
''' First generate a test csv file '''
# import fake_poi_list_generator as fakepoi
# fake_file = fakepoi.make_fake_poi_csv('sample_poi.csv', n=20)

''' Example for generating a kml file '''
# db = POIdb(fake_file)
# db.set_home('1200 E California Blvd, Pasadena, CA 91125')
# db.filter(miles=25)
# db.to_kml(filename='poi_near')
# print(db.sort(by='Name'))
