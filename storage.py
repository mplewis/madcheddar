from config import DATABASE_URI, FAKE_BACKEND
if FAKE_BACKEND:
    from fake_backend import hashed_txns
else:
    from mint_backend import hashed_txns
from processing import hash_txn

import dataset

from functools import lru_cache


db = dataset.connect(DATABASE_URI)
txn_table = db['transactions']


@lru_cache()
def new_txns():
    available_txns_by_hash = hashed_txns()
    available_txn_hashes = set(available_txns_by_hash.keys())
    existing_txn_hashes = set([row['hash'] for row in txn_table.all()])
    new_txn_hashes = available_txn_hashes - existing_txn_hashes
    new_txns = [available_txns_by_hash[h] for h in new_txn_hashes]
    return new_txns


def persist_new_txns():
    for raw_txn in new_txns():
        # Get Dataframe row and convert to Python dict
        txn = raw_txn.to_dict()
        # Add hash
        txn['hash'] = hash_txn(raw_txn)
        # Convert numpy timestamp to Python datetime
        txn['date'] = txn['date'].to_pydatetime()
        # Ensure NaNs are Nulls so string columns don't become floats
        for col in txn.keys():
            if not txn[col]:
                txn[col] = None
        txn_table.insert(txn)
