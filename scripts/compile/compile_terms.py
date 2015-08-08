"""
run:
    $ python3 -m scripts.compile.compile_terms
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv
from collections import OrderedDict

def extract_terms(obj):
    """
    `obj` is a legislator dict

    Returns: a list of term dicts, each with a bioguide_id to serve as foreign key
    """
    b_id = obj['id']['bioguide']
    termslist = []
    for term in obj['terms']:
        t = OrderedDict({'bioguide_id': b_id})
        t['role']           = term['type']
        t['start']          = term['start']
        t['end']            = term.get('end')
        t['party']          = term['party']
        t['district']       = term.get('district')
        t['senator_class']  = term.get('class')
        t['state']          = term['state']
        t['state_rank']     = term.get('state_rank')
        termslist.append(t)
    return termslist


if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'legislators.yaml'))
    leg_data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'terms.csv')
    with open(fname, 'w') as f:
        termslist = [extract_terms(d) for d in leg_data]
        c = csv.DictWriter(f, fieldnames = list(termslist[0][0].keys()))
        c.writeheader()
        for terms in termslist:
            c.writerows(terms)
