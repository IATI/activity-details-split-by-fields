from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_recipient_country import (
    IATIActivityRecipientCountry,
)
from iati_activity_details_split_by_fields.iati_activity_recipient_region import (
    IATIActivityRecipientRegion,
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
            "recipient_region_code": None,
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
            "recipient_region_code": None,
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
            "recipient_region_code": None,
            "sectors": [],
            "value": 500,
        },
        {
            "recipient_country_code": "GB",
            "recipient_region_code": None,
            "sectors": [],
            "value": 500,
        },
    ] == results


def test_split_by_country_with_incorrect_percentages():
    """Test that country splits work correctly even with percentages that don't sum to 100"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=30),  # 30%
            IATIActivityRecipientCountry(code="GB", percentage=40),  # 40%
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    # Check results with ranges
    assert len(results) == 2
    assert results[0]["recipient_country_code"] == "FR"
    assert 428.57 <= results[0]["value"] <= 428.58
    assert results[1]["recipient_country_code"] == "GB"
    assert 571.42 <= results[1]["value"] <= 571.43
    assert all(r["sectors"] == [] for r in results)


def test_no_split_but_region_set():
    """If an activity only has one region, then no split should happen but the region should appear on the transactions"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=100),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "recipient_region_code": "ASIA",
            "sectors": [],
            "value": 1000,
        }
    ] == results


def test_split_by_region():
    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=50),
            IATIActivityRecipientRegion(code="AFRICA", percentage=50),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    assert [
        {
            "recipient_country_code": None,
            "recipient_region_code": "ASIA",
            "sectors": [],
            "value": 500,
        },
        {
            "recipient_country_code": None,
            "recipient_region_code": "AFRICA",
            "sectors": [],
            "value": 500,
        },
    ] == results


def test_split_by_region_with_incorrect_percentages():
    """Test that region splits work correctly even with percentages that don't sum to 100"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=30),  # 30%
            IATIActivityRecipientRegion(code="AFRICA", percentage=40),  # 40%
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    # Check results with ranges
    assert len(results) == 2
    assert results[0]["recipient_region_code"] == "ASIA"
    assert 428.57 <= results[0]["value"] <= 428.58  # ~42.86% of 1000
    assert results[1]["recipient_region_code"] == "AFRICA"
    assert 571.42 <= results[1]["value"] <= 571.43  # ~57.14% of 1000
    assert all(r["recipient_country_code"] is None for r in results)
    assert all(r["sectors"] == [] for r in results)


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
            "recipient_region_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 1000,
        },
        {
            "recipient_country_code": None,
            "recipient_region_code": None,
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
            "recipient_region_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 500,
        },
        {
            "recipient_country_code": None,
            "recipient_region_code": None,
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 500,
        },
        {
            "recipient_country_code": None,
            "recipient_region_code": None,
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 1000,
        },
    ] == results


def test_split_by_sector_with_incorrect_percentages():
    """Test that sector splits work correctly even with percentages that don't sum to 100"""

    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Henry", percentage=30),  # 30%
            IATIActivitySector(vocabulary="cats", code="Linda", percentage=40),  # 40%
            IATIActivitySector(vocabulary="dogs", code="Rover", percentage=100),  # 100%
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    # Check results with ranges
    assert len(results) == 3

    # Check Henry (cats)
    assert results[0]["sectors"][0]["code"] == "Henry"
    assert results[0]["sectors"][0]["vocabulary"] == "cats"
    assert 428.57 <= results[0]["value"] <= 428.58
    assert results[0]["recipient_country_code"] is None

    # Check Linda (cats)
    assert results[1]["sectors"][0]["code"] == "Linda"
    assert results[1]["sectors"][0]["vocabulary"] == "cats"
    assert 571.42 <= results[1]["value"] <= 571.43
    assert results[1]["recipient_country_code"] is None

    # Check Rover (dogs)
    assert results[2]["sectors"][0]["code"] == "Rover"
    assert results[2]["sectors"][0]["vocabulary"] == "dogs"
    assert results[2]["value"] == 1000
    assert results[2]["recipient_country_code"] is None


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
            "recipient_region_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "FR",
            "recipient_region_code": None,
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "FR",
            "recipient_region_code": None,
            "sectors": [{"code": "Rover", "vocabulary": "dogs"}],
            "value": 500,
        },
        {
            "recipient_country_code": "GB",
            "recipient_region_code": None,
            "sectors": [{"code": "Henry", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "GB",
            "recipient_region_code": None,
            "sectors": [{"code": "Linda", "vocabulary": "cats"}],
            "value": 250,
        },
        {
            "recipient_country_code": "GB",
            "recipient_region_code": None,
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
    # Note: This is now implemented in test_no_double_counting test (with one sector vocab)


def test_no_double_counting():
    """Test that split transactions sum up to original amount"""

    # Create activity with both country and sector splits
    iati_activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=60),
            IATIActivityRecipientCountry(code="GB", percentage=40),
        ],
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Health", percentage=70),
            IATIActivitySector(vocabulary="cats", code="Education", percentage=30),
        ],
    )

    results = iati_activity.get_transactions_split_as_json()

    # Checking total value matches original
    total_value = sum(r["value"] for r in results)
    assert total_value == 1000, f"Total {total_value} should equal original 1000"

    # Checking country totals
    country_totals = {}
    for r in results:
        country = r["recipient_country_code"]
        country_totals[country] = country_totals.get(country, 0) + r["value"]

    assert country_totals["FR"] == 600  # 60% of 1000
    assert country_totals["GB"] == 400  # 40% of 1000

    # Checking sector totals
    sector_totals = {}
    for r in results:
        if r["sectors"]:
            sector = r["sectors"][0]["code"]
            sector_totals[sector] = sector_totals.get(sector, 0) + r["value"]

    assert sector_totals["Health"] == 700  # 70% of 1000
    assert sector_totals["Education"] == 300  # 30% of 1000
