from typing import List, Optional

from .iati_activity_transaction_recipient_country import (
    IATIActivityTransactionRecipientCountry,
)
from .iati_activity_transaction_recipient_region import (
    IATIActivityTransactionRecipientRegion,
)
from .iati_activity_transaction_sector import IATIActivityTransactionSector


class IATIActivityTransaction:

    def __init__(
        self,
        value=None,
        sectors: List[IATIActivityTransactionSector] = [],
        recipient_country: Optional[IATIActivityTransactionRecipientCountry] = None,
        recipient_region: Optional[IATIActivityTransactionRecipientRegion] = None,
    ):
        self.value = value
        self.sectors: List[IATIActivityTransactionSector] = sectors
        self.recipient_country: Optional[IATIActivityTransactionRecipientCountry] = (
            recipient_country
        )
        self.recipient_region: Optional[IATIActivityTransactionRecipientRegion] = (
            recipient_region
        )

    def get_as_json(self):
        return {
            "value": self.value,
            "recipient_country": (
                self.recipient_country.get_as_json() if self.recipient_country else None
            ),
            "recipient_region": (
                self.recipient_region.get_as_json() if self.recipient_region else None
            ),
            "sectors": [i.get_as_json() for i in self.sectors],
        }
