from faker import Faker
import usaddress
import phonenumbers as pn
import pandas as pd
import random
from pathlib import Path

OUTPUT_DIR = 'output'

def new_record():
	fake = Faker('en_US')
	company = fake.company()
	address = fake.address().replace('\n',', ')
	g = usaddress.tag(address)[0]
	city = g.get('PlaceName')
	state = g.get('StateName')
	zip = g.get('ZipCode')
	phone = fake.phone_number()
	phone = pn.format_number(pn.parse(phone, 'US'),
		pn.PhoneNumberFormat.NATIONAL)
	lat,lng = fake.latlng()
	review_count = random.randint(1,300)
	return (company, address, city, state, zip,
		phone, float(lat), float(lng), review_count)

def make_fake_poi_csv(filename, n):
	records = []
	for i in range(n):
		records.append(new_record())

	header = ['Name',
			'Address',
			'City',
			'State',
			'Zip',
			'Phone',
			'Latitude',
			'Longitude',
			'Review Count',]
	df = pd.DataFrame.from_records(records, columns=header)
	# print(df)
	output_dir = Path('.', 'output')
	output_dir.mkdir(parents=True, exist_ok=True)
	df.to_csv(output_dir/filename, index=False)
	return Path(output_dir/filename)

# SAMPLE_FILENAME = 'sample_poi.csv'
# make_poi_csv(SAMPLE_FILENAME, n=50)
