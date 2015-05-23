import hashlib


def hash_txn(txn):
    string_attrs = ['isoformat', 'description', 'original_description',
                    'transaction_type', 'category', 'account_name']
    float_attrs = ['amount']
    m = hashlib.sha256()

    for attr in string_attrs:
        value = getattr(txn, attr, None)
        if value:
            try:
                m.update(value.encode())
            except AttributeError:
                pass

    for attr in float_attrs:
        value = getattr(txn, attr, None)
        if value:
            try:
                m.update('{0:.2f}'.format(txn.amount).encode())
            except AttributeError:
                pass

    return m.hexdigest()
