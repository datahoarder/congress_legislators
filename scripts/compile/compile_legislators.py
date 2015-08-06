"""
run:
    $ python3 -m scripts.compile.compile_legislators
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv
from glob import glob
from collections import OrderedDict


def extract_legislator(obj):
    """
    `obj` is a legislator dict

    Returns: a new dict, with filtered/flattened select fields
    """
    h = OrderedDict()
    h['bioguide_id']    = obj['id']['bioguide']
    h['senate_lis_id']  = obj['id'].get('lis')
    h['first_name']     = obj['name'].get('first')
    h['middle_name']    = obj['name'].get('middle')
    h['last_name']      = obj['name'].get('last')
    h['suffix_name']    = obj['name'].get('suffix')
    h['nickname']       = obj['name'].get('nickname')
    h['gender']         = obj['bio'].get('gender')
    h['birthday']       = obj['bio'].get('birthday')
    h['thomas_id']      = obj['id'].get('thomas')
    h['govtrack_id']    = obj['id'].get('govtrack')
    h['opensecrets_id'] = obj['id'].get('opensecrets')

    # add simplified term information
    current_term = max(obj['terms'], key = lambda t: t['start'])
    h['party']               = current_term.get('party')
    h['role']        = current_term.get('type')
    h['state']               = current_term.get('state')
    h['district']            = current_term.get('district')
    h['senate_class']        = current_term.get('class')
    h['state_rank']          = current_term.get('state_rank')
    h['current_term_start']  = current_term.get('start')
    h['current_term_end']    = current_term.get('end')
    h['url']                 = current_term.get('url')
    h['address']             = current_term.get('address')
    h['phone']               = current_term.get('phone')
    h['fax']                 = current_term.get('fax')
    h['contact_form']        = current_term.get('contact_form')
    h['rss_url']             = current_term.get('rss_url')
    return h


if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'legislators.yaml'))
    leg_data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'legislators.csv')
    with open(fname, 'w') as f:
        legislators = [extract_legislator(d) for d in leg_data]
        c = csv.DictWriter(f, fieldnames = list(legislators[0].keys()))
        c.writeheader()
        c.writerows(legislators)
