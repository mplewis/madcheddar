from config import FAKE_BACKEND

if FAKE_BACKEND:
    print('*** Using fake backend! ***')
    from fake_backend import net_worth
else:
    from mint_backend import net_worth
from storage import new_txns as _new_txns, persist_new_txns


def format_txn(txn):
    if txn.transaction_type == 'debit':
        amt = '({:8.2f})'.format(txn.amount)
    else:
        amt = ' {:8.2f} '.format(txn.amount)

    raw_desc = txn.original_description[:20].strip()

    return '{}: {} ({:.20})'.format(
        amt, txn.description, raw_desc)


def main():
    new_txns = _new_txns()
    if not new_txns:
        print('No new transactions')
        return

    new_txns.sort(key=lambda t: t.date, reverse=True)
    for txn in new_txns:
        print(format_txn(txn))

    print('${}'.format(round(net_worth(), 2)))

    persist_new_txns()


if __name__ == '__main__':
    main()
