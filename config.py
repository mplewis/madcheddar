import yaml

import os


with open(os.path.expanduser('~/.madcheddar')) as f:
    user_config = yaml.load(f.read())


FAKE_BACKEND = os.getenv('FAKE_BACKEND', False)

MINT_EMAIL = user_config['mint_email']
MINT_PASSWORD = user_config['mint_password']
DATABASE_URI = user_config['database_uri']
