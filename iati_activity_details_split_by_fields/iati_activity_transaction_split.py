from typing import List, Optional

from .iati_activity_transaction import IATIActivityTransaction
from .iati_activity_transaction_sector import IATIActivityTransactionSector


class IATIActivityTransactionSplit:

    def __init__(
        self,
        value=None,
        sectors: List[IATIActivityTransactionSector] = [],
        recipient_country_code=None,
        iati_activity_transaction: Optional[IATIActivityTransaction] = None,
    ):
        self.value = value
        self.sectors: List[IATIActivityTransactionSector] = sectors
        self.recipient_country_code = recipient_country_code
        if iati_activity_transaction:
            self.value = iati_activity_transaction.value
            self.sectors = iati_activity_transaction.sectors
            self.recipient_country_code = (
                iati_activity_transaction.recipient_country_code
            )

    def get_as_json(self):
        return {
            "value": self.value,
            "recipient_country_code": self.recipient_country_code,
            "sectors": [i.get_as_json() for i in self.sectors],
        }
