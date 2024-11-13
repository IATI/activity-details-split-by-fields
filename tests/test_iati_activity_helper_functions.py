from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_sector import (
    IATIActivitySector,
)


def test_get_sectors_grouped_by_vocab_with_normalised_percentages():

    iati_activity = IATIActivity(
        sectors=[
            IATIActivitySector(vocabulary="cats", code="Henry"),
            IATIActivitySector(vocabulary="cats", code="Linda"),
            IATIActivitySector(vocabulary="dogs", code="Rover"),
        ]
    )

    results = iati_activity._get_sectors_grouped_by_vocab_with_normalised_percentages()

    assert ["Henry", "Linda"] == [i.code for i in results["cats"]]
    assert ["Rover"] == [i.code for i in results["dogs"]]
