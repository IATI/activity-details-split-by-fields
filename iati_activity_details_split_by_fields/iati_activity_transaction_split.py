from typing import List, Optional

from .iati_activity_transaction import IATIActivityTransaction
from .iati_activity_transaction_recipient_country import (
    IATIActivityTransactionRecipientCountry,
)
from .iati_activity_transaction_recipient_region import (
    IATIActivityTransactionRecipientRegion,
)
from .iati_activity_transaction_sector import IATIActivityTransactionSector


class IATIActivityTransactionSplit:

    def __init__(
        self,
        value=None,
        sectors: List[IATIActivityTransactionSector] = [],
        recipient_country: Optional[IATIActivityTransactionRecipientCountry] = None,
        recipient_region: Optional[IATIActivityTransactionRecipientRegion] = None,
        iati_activity_transaction: Optional[IATIActivityTransaction] = None,
    ):
        self.value = value
        self.sectors: List[IATIActivityTransactionSector] = sectors
        self.recipient_country: Optional[IATIActivityTransactionRecipientCountry] = (
            recipient_country
        )
        self.recipient_region: Optional[IATIActivityTransactionRecipientRegion] = (
            recipient_region
        )
        if iati_activity_transaction:
            self.value = iati_activity_transaction.value
            self.sectors = iati_activity_transaction.sectors
            self.recipient_country = (
                IATIActivityTransactionRecipientCountry(
                    iati_activity_recipient_country=iati_activity_transaction.recipient_country
                )
                if iati_activity_transaction.recipient_country
                else None
            )
            self.recipient_region = (
                IATIActivityTransactionRecipientRegion(
                    iati_activity_recipient_region=iati_activity_transaction.recipient_region
                )
                if iati_activity_transaction.recipient_region
                else None
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
