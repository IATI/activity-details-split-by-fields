from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_recipient_country import (
    IATIActivityRecipientCountry,
)
from iati_activity_details_split_by_fields.iati_activity_recipient_region import (
    IATIActivityRecipientRegion,
)
from iati_activity_details_split_by_fields.iati_activity_transaction import (
    IATIActivityTransaction,
)
from iati_activity_details_split_by_fields.iati_activity_transaction_sector import (
    IATIActivityTransactionSector,
)
from iati_activity_details_split_by_fields.worker import Worker


def test_country_set():

    iati_activity = IATIActivity(
        transactions=[
            IATIActivityTransaction(
                value=1000, recipient_country=IATIActivityRecipientCountry(code="GB")
            )
        ],
    )

    worker = Worker()
    results = worker.get_split_transactions_as_json(iati_activity)

    assert [
        {
            "recipient_country": {"code": "GB"},
            "recipient_region": None,
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_region_set():

    iati_activity = IATIActivity(
        transactions=[
            IATIActivityTransaction(
                value=1000, recipient_region=IATIActivityRecipientRegion(code="1")
            )
        ],
    )

    worker = Worker()
    results = worker.get_split_transactions_as_json(iati_activity)

    assert [
        {
            "recipient_country": None,
            "recipient_region": {"code": "1", "vocabulary": "1"},
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_sector_set():

    iati_activity = IATIActivity(
        transactions=[
            IATIActivityTransaction(
                value=1000,
                sectors=[IATIActivityTransactionSector(code="Henry")],
            )
        ],
    )

    worker = Worker()
    results = worker.get_split_transactions_as_json(iati_activity)

    assert [
        {
            "recipient_country": None,
            "recipient_region": None,
            "sectors": [{"code": "Henry", "vocabulary": "1"}],
            "value": 1000,
        },
    ] == results
