"""
run:
    $ python3 -m scripts.compile.compile_committee_memberships

The committee-memberships.yaml looks like:

HLIG:
- name: Devin Nunes
  party: majority
  rank: 1
  title: Chair
  bioguide: N000181
  thomas: '01710'
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv
from collections import OrderedDict

MEMBER_FIELDS_MAP = OrderedDict([["bioguide_id", "bioguide"],
    ["member_thomas_id", "thomas"],
    ["rank", "rank"],
    ["member_name", "name"],
    ["party", "party"],
    ["title", "title"]
    ])
def extract_memberships(comid, members):
    """
    `comid` is the Thomas ID of the committee, e.g. HLIG
    `members` is a list of member dicts

    Returns: a dict containing code and keys from MEMBER_FIELDS_MAP
    """
    arr = []
    for m in members:
        d = {'committee_thomas_id': comid}
        arr.append(d)
        for k, x in MEMBER_FIELDS_MAP.items():
            d[k] = m.get(x)
    return arr

if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'committee-memberships.yaml'))
    data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'committee-memberships.csv')
    with open(fname, 'w') as f:
        cdata = []
        for c, members in data.items():
            cdata.extend(extract_memberships(c, members))
        c = csv.DictWriter(f,
            fieldnames = ['committee_thomas_id'] + list(MEMBER_FIELDS_MAP.keys()) )
        c.writeheader()
        c.writerows(cdata)
