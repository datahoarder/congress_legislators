import os

DATA_DIR = "./stash/"
FETCHED_DIR = os.path.join(DATA_DIR, "fetched")
COMPILED_DIR = os.path.join(DATA_DIR, "compiled")

SOURCE_DATA_URLS = {
    'legislators': 'https://github.com/dannguyen/congress-legislators/raw/master/legislators-current.yaml',
    'social-media-accounts': 'https://raw.githubusercontent.com/dannguyen/congress-legislators/master/legislators-social-media.yaml',
    'committee-memberships': 'https://github.com/unitedstates/congress-legislators/raw/master/committee-membership-current.yaml',
    'committees': 'https://github.com/unitedstates/congress-legislators/raw/master/committees-current.yaml'
}



PACKAGED_DIR = os.path.join(DATA_DIR, "packaged")
## meta data
SCHEMAS_DIR = "./meta/schemas"


def setup_space():
    os.makedirs(FETCHED_DIR, exist_ok = True)
    os.makedirs(COMPILED_DIR, exist_ok = True)
    os.makedirs(PACKAGED_DIR, exist_ok = True)


