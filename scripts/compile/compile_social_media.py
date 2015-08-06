"""
run:
    $ python3 -m scripts.compile.compile_social_media
"""
from scripts.settings import setup_space
from scripts.settings import COMPILED_DIR, FETCHED_DIR
import os.path
import yaml
import csv
from glob import glob
from collections import OrderedDict

SOC_MEDIA_FIELDS = [s + '_' + x for s in ['twitter', 'facebook', 'youtube', 'instagram'] for x in ['id', 'username']]

def extract_member_social_media_info(obj):
    """
    `obj` is a social media dict from:
    - id:
        bioguide: E000295
        thomas: '02283'
        govtrack: 412667
    social:
        twitter: SenJoniErnst
        facebook: senjoniernst
        facebook_id: '351671691660938'
        youtube_id: UCLwrmtF_84FIcK3TyMs4MIw
        instagram: senjoniernst
        instagram_id: 1582702853

    Returns: a dict including bioguide_id as a foreign key
    """
    d = {'bioguide_id': obj['id']['bioguide']}
    s = obj['social']
    for n in ['twitter', 'facebook', 'youtube', 'instagram']:
        d[n + '_username'] = s.get(n)
        d[n + '_id'] = s.get(n + '_id')
    return d

if __name__ == '__main__':
    infile = open(os.path.join(FETCHED_DIR, 'social-media-accounts.yaml'))
    soc_data = yaml.load(infile)
    fname = os.path.join(COMPILED_DIR, 'social-media-accounts.csv')
    with open(fname, 'w') as f:
        socaccounts = [extract_member_social_media_info(d) for d in soc_data]
        c = csv.DictWriter(f,
            fieldnames = ['bioguide_id'] + SOC_MEDIA_FIELDS)
        c.writeheader()
        c.writerows(socaccounts)
