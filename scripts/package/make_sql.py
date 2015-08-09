# An early attempt at using SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData, Index
from sqlalchemy import Integer, String, Boolean, Date
from scripts.settings import setup_space, PACKAGED_DIR, SCHEMAS_DIR, COMPILED_DIR
import csv
import os.path
import rtyaml
from datetime import datetime

engine = create_engine('sqlite:///' + os.path.join(PACKAGED_DIR, 'congress_legislators.sqlite'))
metadata = MetaData()


SCHEMA_TO_DATA_MAP= {
    'committee_memberships': 'committee-memberships.csv',
    'committees': 'committees.csv',
    'fec_ids': 'fec_ids.csv',
    'legislators': 'legislators.csv',
    'social_media_accounts': 'social-media-accounts.csv',
    'terms': 'terms.csv'
}


for schema_name, data_fname in SCHEMA_TO_DATA_MAP.items():
    # Create legislators
    schema = rtyaml.load(open(os.path.join(SCHEMAS_DIR, schema_name + '.yaml')))
    schema_pkeys = schema['db'].get('primary_key')
    # set up schema
    table_name = schema['name']
    table_cols = []

    for c_name, c_meta in schema['columns'].items():
        t = c_meta['type']
        # set type
        if t in ['String', 'Integer', 'Boolean', 'Date']:
            ctype = eval(t)
        else:
            raise Exception("Unrecognized column type:", t)
        # set other attributes
        nullable = False if c_meta.get('nullable') is False else True
        primary_key = True if c_name in schema_pkeys else False
        table_cols.append(
                Column(c_name, ctype, nullable = nullable, primary_key = primary_key ))




    # init table object
    # table = Table(table_name, metadata, *table_cols)
    table = Table(table_name, metadata, *table_cols)
    table.create(engine)
#    metadata.create_all(engine)

    # insert data
    data = list(csv.DictReader(open(os.path.join(COMPILED_DIR, data_fname))))
    for d in data:
        for key, val in d.items():
            if schema['columns'][key]['type'] == 'Date':
                v = datetime.strptime(val, schema['columns'][key]['format'])
                d[key] = v
    conn = engine.connect()
    result = conn.execute(table.insert(), data)



    # Make indexes
    indexes = []
    indexarr = schema['db'].get('indexes')
    if indexarr:
        for i in indexarr:
            arr = i if type(i) is list else [i]
            index_name = table_name + '-' + ('_'.join(arr))
            idx = Index(index_name, *[eval('table.c.' + x) for x in arr])
            idx.create(engine)
            # idx = Index(index_name, *arr)
            # indexes.append(idx)
