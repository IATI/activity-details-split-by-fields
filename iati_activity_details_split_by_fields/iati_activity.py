import xml.etree.ElementTree as ET
from typing import List, Optional

from .iati_activity_recipient_country import IATIActivityRecipientCountry
from .iati_activity_recipient_region import IATIActivityRecipientRegion
from .iati_activity_sector import IATIActivitySector
from .iati_activity_transaction import IATIActivityTransaction
from .iati_activity_transaction_recipient_country import (
    IATIActivityTransactionRecipientCountry,
)
from .iati_activity_transaction_recipient_region import (
    IATIActivityTransactionRecipientRegion,
)
from .iati_activity_transaction_sector import IATIActivityTransactionSector


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

    def get_as_json(self):
        return {
            "recipient_countries": [
                rc.get_as_json() for rc in self.recipient_countries
            ],
            "recipient_regions": [rr.get_as_json() for rr in self.recipient_regions],
            "sectors": [s.get_as_json() for s in self.sectors],
            "transactions": [t.get_as_json() for t in self.transactions],
        }

    @staticmethod
    def from_iati_xml(input: str):
        root = ET.fromstring(input)

        transactions: List[IATIActivityTransaction] = []
        sectors: List[IATIActivitySector] = []
        recipient_countries: List[IATIActivityRecipientCountry] = []
        recipient_regions: List[IATIActivityRecipientRegion] = []

        for child in root:
            if child.tag.lower() == "recipient-region":
                recipient_regions.append(
                    IATIActivityRecipientRegion(
                        vocabulary=child.attrib.get("vocabulary"),
                        code=child.attrib.get("code"),
                        percentage=float(child.attrib.get("percentage", "100")),
                    )
                )
            elif child.tag.lower() == "recipient-country":
                recipient_countries.append(
                    IATIActivityRecipientCountry(
                        code=child.attrib.get("code"),
                        percentage=float(child.attrib.get("percentage", "100")),
                    )
                )
            elif child.tag.lower() == "sector":
                sectors.append(
                    IATIActivitySector(
                        vocabulary=child.attrib.get("vocabulary"),
                        code=child.attrib.get("code"),
                        percentage=float(child.attrib.get("percentage", "100")),
                    )
                )
            elif child.tag.lower() == "transaction":
                transaction_value = None
                transaction_sectors: List[IATIActivityTransactionSector] = []
                transaction_recipient_country: Optional[
                    IATIActivityTransactionRecipientCountry
                ] = None
                transaction_recipient_region: Optional[
                    IATIActivityTransactionRecipientRegion
                ] = None
                for transaction_child in child:
                    if transaction_child.tag.lower() == "recipient-region":
                        transaction_recipient_region = (
                            IATIActivityTransactionRecipientRegion(
                                vocabulary=transaction_child.attrib.get("vocabulary"),
                                code=transaction_child.get("code"),
                            )
                        )
                    elif transaction_child.tag.lower() == "recipient-country":
                        transaction_recipient_country = (
                            IATIActivityTransactionRecipientCountry(
                                code=transaction_child.attrib.get("code"),
                            )
                        )
                    elif transaction_child.tag.lower() == "sector":
                        transaction_sectors.append(
                            IATIActivityTransactionSector(
                                vocabulary=transaction_child.attrib.get("vocabulary"),
                                code=transaction_child.attrib.get("code"),
                            )
                        )
                    elif transaction_child.tag.lower() == "value":
                        transaction_value = float(transaction_child.text or "")
                transactions.append(
                    IATIActivityTransaction(
                        value=transaction_value,
                        sectors=transaction_sectors,
                        recipient_country=transaction_recipient_country,
                        recipient_region=transaction_recipient_region,
                    )
                )

        return IATIActivity(
            transactions=transactions,
            sectors=sectors,
            recipient_countries=recipient_countries,
            recipient_regions=recipient_regions,
        )
