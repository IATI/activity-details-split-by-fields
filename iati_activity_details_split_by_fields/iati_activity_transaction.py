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
