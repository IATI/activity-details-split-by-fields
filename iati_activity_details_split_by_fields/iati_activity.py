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
        output = []

        for transaction in self.transactions:
            # Print initial transaction details
            print(f"Processing transaction: {transaction.value}")
            
            # If transaction has its own recipient or sector declarations, use it directly
            if (
                transaction.recipient_country_code is not None or 
                transaction.recipient_region_code is not None or 
                transaction.sectors
            ):
                output.append(IATIActivityTransactionSplit(iati_activity_transaction=transaction))
                continue

            # Get recipient groups (by vocab), with percentages normalized per group
            vocab_groups = self._get_recipients_grouped_by_vocab_with_normalised_percentages()
            print("Vocab Groups: ", vocab_groups)  # See the grouped recipients by vocab

            # If no recipients, keep original transaction
            if not vocab_groups:
                output.append(IATIActivityTransactionSplit(iati_activity_transaction=transaction))
                continue

            # For each vocabulary, split the full transaction value among recipients in that group
            for vocab, recipients in vocab_groups.items():
                for recipient in recipients:
                    split = IATIActivityTransactionSplit()
                    split.value = transaction.value * recipient["percentage"] / 100

                    if recipient["type"] == "country":
                        split.recipient_country_code = recipient["code"]
                        split.recipient_region_code = None
                    else:
                        split.recipient_region_code = recipient["code"]
                        split.recipient_country_code = None

                    # Print each split to inspect how it's being calculated
                    print(f"Split transaction for {vocab} - {recipient['type']} {recipient['code']}: {split.value}")
                    output.append(split)

        # If there are sectors to split by, handle them
        if self.sectors:
            sectors_grouped = self._get_sectors_grouped_by_vocab_with_normalised_percentages()
            print("Sectors Grouped: ", sectors_grouped)  # See how sectors are being grouped

            new_output = []
            for split_transaction in output:
                # If split already has sectors, leave as is
                if split_transaction.sectors:
                    new_output.append(split_transaction)
                    continue

                has_sector_splits = False

                for vocab, sectors in sectors_grouped.items():
                    for sector in sectors:
                        has_sector_splits = True
                        sector_split = copy.deepcopy(split_transaction)
                        sector_split.value = split_transaction.value * sector.percentage / 100
                        sector_split.sectors = [
                            IATIActivityTransactionSector(iati_activity_sector=sector)
                        ]
                        new_output.append(sector_split)

                # If no sector was applied, keep the original
                if not has_sector_splits:
                    new_output.append(split_transaction)

            output = new_output

        # Print the final output before returning
        print("Final Output Transactions: ", output)
        
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

    def _get_recipients_grouped_by_vocab_with_normalised_percentages(self) -> dict:
        """
        Group countries and regions by vocabulary and normalise percentages within each group.
        Returns a dictionary where each key is a vocabulary (string), and each value is a list
        of recipient dicts with 'type', 'code', 'percentage', and 'object'.
        """
        vocab_groups = {}

        # Group recipient countries under vocab "1" only
        if self.recipient_countries:
            vocab = "1"
            if vocab not in vocab_groups:
                vocab_groups[vocab] = []
            
            for country in self.recipient_countries:
                vocab_groups[vocab].append({
                    "type": "country",
                    "code": country.code,
                    "percentage": country.percentage or 0,
                    "object": copy.deepcopy(country),
                })

        # Group recipient regions by their declared vocabulary, defaulting to "1"
        if self.recipient_regions:
            for region in self.recipient_regions:
                vocab = region.vocabulary or "1"
                if vocab not in vocab_groups:
                    vocab_groups[vocab] = []
                
                vocab_groups[vocab].append({
                    "type": "region",
                    "code": region.code,
                    "percentage": region.percentage or 0,
                    "object": copy.deepcopy(region),
                })

        # Normalise percentages per vocabulary group
        for vocab, recipients in vocab_groups.items():
            total = sum(r["percentage"] for r in recipients)
            if total > 0:
                for recipient in recipients:
                    recipient["percentage"] = (recipient["percentage"] / total) * 100

        return vocab_groups