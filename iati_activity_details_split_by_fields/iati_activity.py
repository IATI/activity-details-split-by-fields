import copy
from typing import List

from .iati_activity_recipient_country import IATIActivityRecipientCountry
from .iati_activity_recipient_region import IATIActivityRecipientRegion
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
        recipient_regions: List[IATIActivityRecipientRegion] = [],
    ):
        self.transactions: List[IATIActivityTransaction] = transactions
        self.sectors: List[IATIActivitySector] = sectors
        self.recipient_countries: List[IATIActivityRecipientCountry] = (
            recipient_countries
        )
        self.recipient_regions: List[IATIActivityRecipientRegion] = recipient_regions

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
        if len(self.recipient_regions) >= 1:
            new_output = []
            for transaction in output:
                for (
                    recipient_region
                ) in self._get_recipient_regions_with_normalised_percentages():
                    split_transaction = copy.deepcopy(transaction)
                    split_transaction.value = (
                        split_transaction.value * recipient_region.percentage / 100
                    )
                    split_transaction.recipient_region_code = recipient_region.code
                    new_output.append(split_transaction)
            output = new_output

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
        """Normalise country percentages to ensure they sum to 100%"""
        if not self.recipient_countries:
            return []
        total_percentage = sum(
            country.percentage or 0 for country in self.recipient_countries
        )
        if total_percentage == 0:
            return self.recipient_countries

        normalized_countries = copy.deepcopy(self.recipient_countries)

        for country in normalized_countries:
            if country.percentage:
                country.percentage = (country.percentage / total_percentage) * 100

        return normalized_countries

    def _get_sectors_grouped_by_vocab_with_normalised_percentages(self) -> dict:
        """Group sectors by vocabulary and normalise percentages within each group"""
        if not self.sectors:
            return {}

        # First group by vocab
        grouped: dict = {}
        for sector in self.sectors:
            vocab = sector.vocabulary or "default"
            if vocab not in grouped:
                grouped[vocab] = []
            grouped[vocab].append(copy.deepcopy(sector))

        # Now normalise percentages within each vocab group
        for vocab, sectors in grouped.items():
            total = sum(sector.percentage or 0 for sector in sectors)
            if total > 0:  # we only normalise if we have valid percentages
                for sector in sectors:
                    if sector.percentage:
                        sector.percentage = (sector.percentage / total) * 100

        return grouped

    def _get_recipient_regions_with_normalised_percentages(self):
        """Normalise region percentages to ensure they sum to 100%"""
        if not self.recipient_regions:
            return []
        total_percentage = sum(
            region.percentage or 0 for region in self.recipient_regions
        )
        if total_percentage == 0:
            return self.recipient_regions

        normalized_regions = copy.deepcopy(self.recipient_regions)

        for region in normalized_regions:
            if region.percentage:
                region.percentage = (region.percentage / total_percentage) * 100

        return normalized_regions
