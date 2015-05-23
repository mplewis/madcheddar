from config import MINT_EMAIL, MINT_PASSWORD
from processing import hash_txn

import mintapi

from functools import lru_cache


@lru_cache()
def _mint():
    mint = mintapi.Mint(MINT_EMAIL, MINT_PASSWORD)
    return mint


@lru_cache()
def _accounts():
    return _mint().get_accounts()


@lru_cache()
def _txns():
    return _mint().get_transactions()


def net_worth():
    total = 0
    for account in _accounts():
        value = account['value']
        if account['accountType'] == 'loan':
            total -= value
        else:
            total += value
    return total


def hashed_txns():
    hashed = {}
    for index, txn in _txns().iterrows():
        txn_hash = hash_txn(txn)
        hashed[txn_hash] = txn
    return hashed
