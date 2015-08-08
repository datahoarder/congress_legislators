"""
run:
    $ python3 -m scripts.fetch.fetch_data

Fetches member, committee, and social media data from unitedstates/congress-legislators
"""
from scripts.settings import setup_space
from scripts.settings import FETCHED_DIR
from scripts.settings import SOURCE_DATA_URLS
import os.path
import requests



if __name__ == '__main__':
    setup_space()
    for slug, url in SOURCE_DATA_URLS.items():
        print("----------")
        print("Downloading", url)
        resp = requests.get(url)
        fname = os.path.join(FETCHED_DIR, slug +'.yaml')
        with open(fname, 'w') as f:
            print("Writing", fname)
            f.write(resp.text)
