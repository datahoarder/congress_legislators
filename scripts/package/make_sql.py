# An early attempt at using SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Integer, String, Boolean, Date
from scripts.settings import setup_space, PACKAGED_DIR, SCHEMAS_DIR, COMPILED_DIR
import csv
import os.path
import rtyaml
from datetime import datetime

engine = create_engine('sqlite:///' + os.path.join(PACKAGED_DIR, 'congress_legislators.sqlite'))
metadata = MetaData()


# Create legislators
leg_schema = rtyaml.load(open(os.path.join(SCHEMAS_DIR, 'legislators.yaml')))

# set up schema
table_name = leg_schema['name']
table_cols = []
for c_name, c_meta in leg_schema['columns'].items():
    t = c_meta['type']
    if t in ['String', 'Integer', 'Boolean', 'Date']:
        ctype = eval(t)
    else:
        raise Exception("Unrecognized column type:", t)
    table_cols.append(Column(c_name, ctype))
# init table object
table = Table(table_name, metadata, *table_cols)
metadata.create_all(engine)

# insert data
leg_data = list(csv.DictReader(open(os.path.join(COMPILED_DIR, 'legislators.csv'))))
for d in leg_data:
    for key, val in d.items():
        if leg_schema['columns'][key]['type'] == 'Date':
            v = datetime.strptime(val, leg_schema['columns'][key]['format'])
            d[key] = v

conn = engine.connect()
result = conn.execute(table.insert(), leg_data)
