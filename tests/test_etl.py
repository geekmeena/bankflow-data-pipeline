from src.etl import transform


def test_duplicate_removal():
    transactions = [
        {"transaction_id": "TXN101", "amount": "100"},
        {"transaction_id": "TXN101", "amount": "100"},
        {"transaction_id": "TXN102", "amount": "200"},
    ]

    valid, invalid = transform(transactions)

    assert len(valid) == 2
    assert len(invalid) == 0

def test_missing_amount():
    transactions = [
        {"transaction_id": "TXN101", "amount": "100"},
        {"transaction_id": "TXN102", "amount": ""},
    ]

    valid, invalid = transform(transactions)

    assert len(valid) == 1
    assert len(invalid) == 1
    assert invalid[0]["transaction_id"] == "TXN102"    