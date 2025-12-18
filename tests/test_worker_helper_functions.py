from iati_activity_details_split_by_fields.iati_activity_recipient_country import (
    IATIActivityRecipientCountry,
)
from iati_activity_details_split_by_fields.iati_activity_recipient_region import (
    IATIActivityRecipientRegion,
)
from iati_activity_details_split_by_fields.iati_activity_sector import (
    IATIActivitySector,
)
from iati_activity_details_split_by_fields.worker import Worker


def test_get_sectors_grouped_by_vocab_with_normalised_percentages():

    sectors = [
        IATIActivitySector(vocabulary="cats", code="Henry", percentage=50),
        IATIActivitySector(vocabulary="cats", code="Linda", percentage=150),
        IATIActivitySector(vocabulary="dogs", code="Rover", percentage=75),
    ]

    worker = Worker()
    results = worker._get_sectors_grouped_by_vocab_with_normalised_percentages(sectors)

    assert ["Henry", "Linda"] == [i.code for i in results["cats"]]
    assert [25, 75] == [i.percentage for i in results["cats"]]
    assert ["Rover"] == [i.code for i in results["dogs"]]
    assert [100] == [i.percentage for i in results["dogs"]]


def test_get_countries_and_regions_grouped_by_vocab_with_normalised_percentages():

    countries = [
        IATIActivityRecipientCountry(code="GB", percentage=50),
        IATIActivityRecipientCountry(code="US", percentage=50),
    ]

    regions = [
        IATIActivityRecipientRegion(code="1", percentage=50, vocabulary="1"),
        IATIActivityRecipientRegion(code="2", percentage=50, vocabulary="1"),
        IATIActivityRecipientRegion(code="1", percentage=5, vocabulary="2"),
        IATIActivityRecipientRegion(code="2", percentage=5, vocabulary="2"),
    ]

    worker = Worker()
    results = (
        worker._get_countries_and_regions_grouped_by_vocab_with_normalised_percentages(
            countries, regions
        )
    )

    assert ["GB", "US"] == [i.code for i in results["1"]["countries"]]
    assert [25, 25] == [i.percentage for i in results["1"]["countries"]]
    assert ["1", "2"] == [i.code for i in results["1"]["regions"]]
    assert [25, 25] == [i.percentage for i in results["1"]["regions"]]

    assert ["GB", "US"] == [i.code for i in results["2"]["countries"]]
    assert [45, 45] == [int(i.percentage) for i in results["2"]["countries"]]
    assert ["1", "2"] == [i.code for i in results["2"]["regions"]]
    assert [4, 4] == [int(i.percentage) for i in results["2"]["regions"]]
