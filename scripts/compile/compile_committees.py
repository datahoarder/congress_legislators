"""
run:
    $ python3 -m scripts.compile.compile_committees

The committees.yaml looks like:
- type: house
  name: House Committee on Agriculture
  url: http://agriculture.house.gov/
  minority_url: http://democrats.agriculture.house.gov/
  thomas_id: HSAG
  house_committee_id: AG
  subcommittees:
  - name: Conservation and Forestry
    thomas_id: '15'
    address: 1301 LHOB; Washington, DC 20515
    phone: (202) 225-2171
  address: 1301 LHOB; Washington, DC 20515-6001
  phone: (202) 225-2171
  rss_url: http://agriculture.house.gov/rss.xml
  minority_rss_url: http://democrats.agriculture.house.gov/Rss.aspx?GroupID=1
  jurisdiction: The House Committee on Agriculture has jurisdiction over federal agriculture
    policy and oversight of some federal agencies, and it can recommend funding appropriations
    for various governmental agencies, programs, and activities, as defined by House
    rules.
  jurisdiction_source: http://en.wikipedia.org/wiki/House_Committee_on_Agriculture
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv
from collections import OrderedDict

LITERAL_FIELD_NAMES = ['type', 'name', 'thomas_id',
    'address', 'phone', 'url', 'minority_url', 'rss_url',
    'minority_rss_url', 'jurisdiction', 'jurisdiction_source'
]

LITERAL_SUBCOMM_FIELD_NAMES = ['name', 'thomas_id', 'address', 'phone']

FIELD_NAMES = ['committee_thomas_id', 'parent_committee_id'] + LITERAL_FIELD_NAMES

def extract_committee(obj):
    arr = []
    d = {}
    for n in LITERAL_FIELD_NAMES:
        d[n] = obj.get(n)
    # don't think I need this...
    # if obj['type'] in ['joint', 'senate']:
    #     d['committee_chamber_id'] = obj['senate_committee_id']
    # else:
    #     d['committee_chamber_id'] = obj['house_committee_id']

    d['committee_thomas_id'] =  d['thomas_id']
    arr.append(d)
    if obj.get('subcommittees'):
        for sub in extract_subcommittees(obj['subcommittees']):
            sub['type'] = d['type']
            sub['parent_committee_id'] = d['committee_thomas_id']
            sub['committee_thomas_id'] = sub['parent_committee_id'] + sub['thomas_id']
            arr.append(sub)
    return arr


def extract_subcommittees(sub_objs):
    arr = []
    for obj in sub_objs:
        s = {}
        arr.append(s)
        for n in LITERAL_SUBCOMM_FIELD_NAMES:
            s[n] = obj.get(n)
    return arr





if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'committees.yaml'))
    data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'committees.csv')
    with open(fname, 'w') as f:
        clist = []
        for coms in data:
            clist.extend(extract_committee(coms))
        c = csv.DictWriter(f, fieldnames = FIELD_NAMES )
        c.writeheader()
        c.writerows(clist)
