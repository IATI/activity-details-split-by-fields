from typing import List

from .iati_activity_recipient_country import IATIActivityRecipientCountry
from .iati_activity_recipient_region import IATIActivityRecipientRegion
from .iati_activity_sector import IATIActivitySector
from .iati_activity_transaction import IATIActivityTransaction


class IATIActivity:

    def __init__(
        self,
        transactions: List[IATIActivityTransaction] = [],
        sectors: List[IATIActivitySector] = [],
        recipient_countries: List[IATIActivityRecipientCountry] = [],
        recipient_regions: List[IATIActivityRecipientRegion] = [],
    ):
        self.transactions: List[IATIActivityTransaction] = transactions
        self.sectors: List[IATIActivitySector] = sectors
        self.recipient_countries: List[IATIActivityRecipientCountry] = (
            recipient_countries
        )
        self.recipient_regions: List[IATIActivityRecipientRegion] = recipient_regions
