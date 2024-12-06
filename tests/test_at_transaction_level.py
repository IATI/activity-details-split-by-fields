from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_transaction import (
    IATIActivityTransaction,
)
from iati_activity_details_split_by_fields.iati_activity_transaction_sector import (
    IATIActivityTransactionSector,
)


def test_country_set():

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000, recipient_country_code="GB")],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": "GB",
            "recipient_region_code": None,
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_sector_set():

    iati_activity = IATIActivity(
        transactions=[
            IATIActivityTransaction(
                value=1000,
                sectors=[
                    IATIActivityTransactionSector(vocabulary="cats", code="Henry")
                ],
            )
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "recipient_region_code": None, 
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 1000,
        },
    ] == results
