"""
run:
    $ python3 -m scripts.compile.compile_fec_ids

    Each congressmember can have one or more FEC IDs
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv


def extract_fec_ids(obj):
    """
    `obj` is a legislator dict

    Returns: a list of dicts, with keys: bioguide_id, fec_id
    """
    b_id = obj['id']['bioguide']
    ids = [{'bioguide_id': b_id, 'fec_id': f_id} for f_id in obj['id'].get('fec')]
    return ids


if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'legislators.yaml'))
    leg_data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'fec_ids.csv')
    with open(fname, 'w') as f:
        flist = [extract_fec_ids(d) for d in leg_data]
        c = csv.DictWriter(f, fieldnames = ['bioguide_id', 'fec_id'])
        c.writeheader()
        for fx in flist:
            c.writerows(fx)
