from processing import hash_txn

from faker import Faker

import inspect
from random import randint
from datetime import datetime


fake = Faker()


class FakeTxn:
    def __init__(self, date, description, original_description, amount,
                 account_name, transaction_type, category, notes, labels):
        self.date = date
        self.description = description
        self.original_description = original_description
        self.amount = amount
        self.account_name = account_name
        self.transaction_type = transaction_type
        self.category = category
        self.notes = notes
        self.labels = labels

    def to_dict(self):
        # From http://stackoverflow.com/a/61522/254187
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                pr[name] = value
        return pr


class FakeTimestamp:
    def __init__(self, dt):
        self.dt = dt

    def to_pydatetime(self):
        return self.dt

    def __lt__(self, other):
        return self.dt < other.dt


def net_worth():
    return float(randint(100000, 999999)) / 100


def hashed_txns():
    if randint(1, 3) == 1:
        return {}

    hashed = {}
    for _ in range(randint(1, 4)):
        txn = FakeTxn(
            FakeTimestamp(datetime.now()),
            fake.company(),
            fake.street_address(),
            float(randint(-10000, 10000)) / 100,
            fake.company(),
            fake.company(),
            fake.company(),
            None,
            None
        )
        hashed[hash_txn(txn)] = txn
    return hashed
