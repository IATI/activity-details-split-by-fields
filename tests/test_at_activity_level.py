from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_recipient_country import (
    IATIActivityRecipientCountry,
)
from iati_activity_details_split_by_fields.iati_activity_sector import (
    IATIActivitySector,
)
from iati_activity_details_split_by_fields.iati_activity_transaction import (
    IATIActivityTransaction,
)


def test_no_split():

    iati_activity = IATIActivity(transactions=[IATIActivityTransaction(value=1000)])

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_no_split_but_country_set():
    """If a activity only has one country, then no split should happen but the country should appear on the transactions"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="GB", percentage=100),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": "GB",
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_split_by_country():

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=50),
            IATIActivityRecipientCountry(code="GB", percentage=50),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": "FR",
            "sectors": [],
            "value": 500,
        },
        {
            "recipient_country_code": "GB",
            "sectors": [],
            "value": 500,
        },
    ] == results


def test_no_split_but_sector_set():
    """If a activity only has one sector (per vocab), then no split should happen but the sectors should appear on the transactions"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Henry", percentage=100),
            IATIActivitySector(vocabulary="dogs", code="Rover", percentage=100),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 1000,
        },
        {
            "recipient_country_code": None,
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 1000,
        },
    ] == results


def test_split_by_sector():

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Henry", percentage=50),
            IATIActivitySector(vocabulary="cats", code="Linda", percentage=50),
            IATIActivitySector(vocabulary="dogs", code="Rover", percentage=100),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 500,
        },
        {
            "recipient_country_code": None,
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 500,
        },
        {
            "recipient_country_code": None,
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 1000,
        },
    ] == results


def test_split_by_everything():
    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Henry", percentage=50),
            IATIActivitySector(vocabulary="cats", code="Linda", percentage=50),
            IATIActivitySector(vocabulary="dogs", code="Rover", percentage=100),
        ],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=50),
            IATIActivityRecipientCountry(code="GB", percentage=50),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": "FR",
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "FR",
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "FR",
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 500,
        },
        {
            "recipient_country_code": "GB",
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "GB",
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "GB",
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 500,
        },
    ] == results

    # TODO could add code to test sum of the values in the results (per sector vocab)
    # add up to the original value set on the transaction.
    # We are then checking NO DOUBLE COUNTING!
    # It's possible to verify this by hand,
    # but may as well get Python to check for us and avoid extra work and the possibility of mistakes
    # (Can use in other tests too)
