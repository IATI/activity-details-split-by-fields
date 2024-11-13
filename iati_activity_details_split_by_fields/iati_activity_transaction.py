from typing import List

from .iati_activity_transaction_sector import IATIActivityTransactionSector


class IATIActivityTransaction:

    def __init__(
        self,
        value=None,
        sectors: List[IATIActivityTransactionSector] = [],
        recipient_country_code=None,
    ):
        self.value = value
        self.sectors: List[IATIActivityTransactionSector] = sectors
        self.recipient_country_code = recipient_country_code
