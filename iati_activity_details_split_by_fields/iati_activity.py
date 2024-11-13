import copy
from typing import List

from .iati_activity_recipient_country import IATIActivityRecipientCountry
from .iati_activity_sector import IATIActivitySector
from .iati_activity_transaction import IATIActivityTransaction
from .iati_activity_transaction_sector import IATIActivityTransactionSector
from .iati_activity_transaction_split import IATIActivityTransactionSplit


class IATIActivity:

    def __init__(
        self,
        transactions: List[IATIActivityTransaction] = [],
        sectors: List[IATIActivitySector] = [],
        recipient_countries: List[IATIActivityRecipientCountry] = [],
    ):
        self.transactions: List[IATIActivityTransaction] = transactions
        self.sectors: List[IATIActivitySector] = sectors
        self.recipient_countries: List[IATIActivityRecipientCountry] = (
            recipient_countries
        )

    def get_transactions_split(self):
        output = [
            IATIActivityTransactionSplit(iati_activity_transaction=i)
            for i in self.transactions
        ]

        # Split by recipient_countries
        if len(self.recipient_countries) >= 1:
            new_output = []
            for transaction in output:
                for (
                    recipient_country
                ) in self._get_recipient_countries_with_normalised_percentages():
                    split_transaction = copy.deepcopy(transaction)
                    split_transaction.value = (
                        split_transaction.value * recipient_country.percentage / 100
                    )
                    split_transaction.recipient_country_code = recipient_country.code
                    new_output.append(split_transaction)
            output = new_output

        # Split by recipient_regions
        # TODO

        # Split by Sectors
        if len(self.sectors) >= 1:
            sectors_grouped = (
                self._get_sectors_grouped_by_vocab_with_normalised_percentages()
            )
            new_output = []
            for transaction in output:
                for vocab, sectors in sectors_grouped.items():
                    for sector in sectors:
                        split_transaction = copy.deepcopy(transaction)
                        split_transaction.value = (
                            split_transaction.value * sector.percentage / 100
                        )
                        split_transaction.sectors = [
                            IATIActivityTransactionSector(iati_activity_sector=sector)
                        ]
                        new_output.append(split_transaction)
            output = new_output

        # Done!
        return output

    def get_transactions_split_as_json(self):
        return [x.get_as_json() for x in self.get_transactions_split()]

    def _get_recipient_countries_with_normalised_percentages(self):
        # TODO
        return self.recipient_countries

    def _get_sectors_grouped_by_vocab_with_normalised_percentages(self) -> dict:
        output: dict = {}
        # Group by vocab
        for sector in self.sectors:
            if sector.vocabulary not in output:
                output[sector.vocabulary] = []
            output[sector.vocabulary].append(sector)
        # Now normalise percentages
        # TODO
        # Ready!
        return output
