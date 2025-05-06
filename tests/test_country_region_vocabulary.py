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


def test_country_region_same_vocabulary():
    """Test that countries and regions in the same vocabulary are treated as a single allocation."""
    activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=25),
            IATIActivityRecipientCountry(code="GB", percentage=25),
        ],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=25),
            IATIActivityRecipientRegion(code="AFRICA", percentage=25),
        ],
    )
    results = activity.get_transactions_split_as_json()
    assert len(results) == 4

    country_fr = next(r for r in results if r["recipient_country_code"] == "FR")
    assert country_fr["value"] == 250

    country_gb = next(r for r in results if r["recipient_country_code"] == "GB")
    assert country_gb["value"] == 250

    region_asia = next(r for r in results if r["recipient_region_code"] == "ASIA")
    assert region_asia["value"] == 250

    region_africa = next(r for r in results if r["recipient_region_code"] == "AFRICA")
    assert region_africa["value"] == 250


def test_multiple_region_vocabularies():
    """Test that multiple region vocabularies create separate allocations."""
    activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=25),
            IATIActivityRecipientCountry(code="GB", percentage=25),
        ],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=25, vocabulary="1"),
            IATIActivityRecipientRegion(code="AFRICA", percentage=25, vocabulary="1"),
            IATIActivityRecipientRegion(code="NORTH", percentage=50, vocabulary="2"),
            IATIActivityRecipientRegion(code="SOUTH", percentage=50, vocabulary="2"),
        ],
    )
    results = activity.get_transactions_split_as_json()
    assert len(results) == 6

    country_fr = next(r for r in results if r["recipient_country_code"] == "FR")
    assert country_fr["value"] == 250

    country_gb = next(r for r in results if r["recipient_country_code"] == "GB")
    assert country_gb["value"] == 250

    region_asia = next(r for r in results if r["recipient_region_code"] == "ASIA")
    assert region_asia["value"] == 250

    region_africa = next(r for r in results if r["recipient_region_code"] == "AFRICA")
    assert region_africa["value"] == 250

    region_north = next(r for r in results if r["recipient_region_code"] == "NORTH")
    assert region_north["value"] == 500

    region_south = next(r for r in results if r["recipient_region_code"] == "SOUTH")
    assert region_south["value"] == 500


def test_incorrect_percentages_normalisation():
    """Test that percentages are normalised correctly within each vocabulary."""
    activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=1000)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="FR", percentage=30),
            IATIActivityRecipientCountry(code="GB", percentage=20),
        ],
        recipient_regions=[
            IATIActivityRecipientRegion(code="ASIA", percentage=40),
            IATIActivityRecipientRegion(code="AFRICA", percentage=10),
        ],
    )
    results = activity.get_transactions_split_as_json()
    assert len(results) == 4

    country_fr = next(r for r in results if r["recipient_country_code"] == "FR")
    assert country_fr["value"] == 300

    country_gb = next(r for r in results if r["recipient_country_code"] == "GB")
    assert country_gb["value"] == 200

    region_asia = next(r for r in results if r["recipient_region_code"] == "ASIA")
    assert region_asia["value"] == 400

    region_africa = next(r for r in results if r["recipient_region_code"] == "AFRICA")
    assert region_africa["value"] == 100


def test_only_countries_no_regions():
    """Test splitting when only countries are provided."""
    activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=500)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="US", percentage=60),
            IATIActivityRecipientCountry(code="CA", percentage=40),
        ],
        recipient_regions=[],
    )
    results = activity.get_transactions_split_as_json()
    assert len(results) == 2

    us = next(r for r in results if r["recipient_country_code"] == "US")
    assert us["value"] == 300

    ca = next(r for r in results if r["recipient_country_code"] == "CA")
    assert ca["value"] == 200


def test_total_split_exceeds_original_due_to_multiple_vocabularies():
    """Test that the total split value can exceed the original when using multiple recipient vocabularies."""
    activity = IATIActivity(
        transactions=[IATIActivityTransaction(value=100)],
        recipient_countries=[
            IATIActivityRecipientCountry(code="X", percentage=50),
        ],
        recipient_regions=[
            IATIActivityRecipientRegion(code="Y", vocabulary="1", percentage=50),
            IATIActivityRecipientRegion(code="Z", vocabulary="2", percentage=50),
        ],
    )
    results = activity.get_transactions_split_as_json()
    assert len(results) == 3

    total_value = sum(r["value"] for r in results)
    assert (
        total_value == 200
    )  # Each vocabulary group is treated independently, so values add up beyond 100
