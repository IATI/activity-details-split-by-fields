import copy

from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_transaction_recipient_country import (
    IATIActivityTransactionRecipientCountry,
)
from iati_activity_details_split_by_fields.iati_activity_transaction_recipient_region import (
    IATIActivityTransactionRecipientRegion,
)
from iati_activity_details_split_by_fields.iati_activity_transaction_sector import (
    IATIActivityTransactionSector,
)
from iati_activity_details_split_by_fields.iati_activity_transaction_split import (
    IATIActivityTransactionSplit,
)


class Worker:

    def __init__(self, region_vocabularies=[], sector_vocabularies=[]):
        self.region_vocabularies = region_vocabularies
        self.sector_vocabularies = sector_vocabularies

    def get_split_transactions(self, iati_activity: IATIActivity):

        # If activity doesn't have any recipient or sector declarations, no splitting is possible
        if (
            len(iati_activity.recipient_countries) == 0
            and len(iati_activity.recipient_regions) == 0
            and len(iati_activity.sectors) == 0
        ):
            return [
                IATIActivityTransactionSplit(iati_activity_transaction=transaction)
                for transaction in iati_activity.transactions
            ]

        # If activity has recipient or sector declarations, split transactions accordingly
        output = []
        sectors_grouped = (
            self._get_sectors_grouped_by_vocab_with_normalised_percentages(
                iati_activity.sectors
            )
        )

        countries_and_regions_grouped = self._get_countries_and_regions_grouped_by_vocab_with_normalised_percentages(
            iati_activity.recipient_countries, iati_activity.recipient_regions
        )

        # For every transaction ....
        for transaction in iati_activity.transactions:

            # If transaction has its own recipient or sector declarations, use it directly
            if (
                transaction.recipient_country is not None
                or transaction.recipient_region is not None
                or transaction.sectors
            ):
                output.append(
                    IATIActivityTransactionSplit(iati_activity_transaction=transaction)
                )
                continue

            # Ok, we split by something ....
            transactions_split = [
                IATIActivityTransactionSplit(iati_activity_transaction=transaction)
            ]

            # Split by Sectors
            if sectors_grouped:
                new_transactions_split = []
                for split_transaction in transactions_split:
                    for vocab, sectors in sectors_grouped.items():
                        for sector in sectors:
                            new_split_transaction = copy.deepcopy(split_transaction)
                            new_split_transaction.value = (
                                new_split_transaction.value * sector.percentage / 100
                            )
                            new_split_transaction.sectors = [
                                IATIActivityTransactionSector(
                                    iati_activity_sector=sector
                                )
                            ]
                            new_transactions_split.append(new_split_transaction)
                transactions_split = new_transactions_split

            # Split by country and regions
            if countries_and_regions_grouped:
                new_transactions_split = []
                for split_transaction in transactions_split:
                    for vocab, data in countries_and_regions_grouped.items():
                        for region in data["regions"]:
                            new_split_transaction = copy.deepcopy(split_transaction)
                            new_split_transaction.value = (
                                new_split_transaction.value * region.percentage / 100
                            )
                            new_split_transaction.recipient_region = (
                                IATIActivityTransactionRecipientRegion(
                                    iati_activity_recipient_region=region
                                )
                            )
                            new_transactions_split.append(new_split_transaction)
                        for country in data["countries"]:
                            new_split_transaction = copy.deepcopy(split_transaction)
                            new_split_transaction.value = (
                                new_split_transaction.value * country.percentage / 100
                            )
                            new_split_transaction.recipient_country = (
                                IATIActivityTransactionRecipientCountry(
                                    iati_activity_recipient_country=country
                                )
                            )
                            new_transactions_split.append(new_split_transaction)

                transactions_split = new_transactions_split

            # Save output
            output.extend(transactions_split)

        return output

    def get_split_transactions_as_json(self, iati_activity: IATIActivity):
        transactions_split = self.get_split_transactions(iati_activity)
        return [transaction.get_as_json() for transaction in transactions_split]

    def _get_sectors_grouped_by_vocab_with_normalised_percentages(
        self, sectors: list
    ) -> dict:
        """Group sectors by vocabulary and normalise percentages within each vocab"""

        # First group by vocab
        grouped: dict = {}
        for sector in sectors:
            vocab = sector.vocabulary or "1"
            if vocab in self.sector_vocabularies or not self.sector_vocabularies:
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

    def _get_countries_and_regions_grouped_by_vocab_with_normalised_percentages(
        self, countries: list, regions: list
    ) -> dict:
        """Group countries and regions by vocabulary (where applicable) and normalise percentages within each vocab"""

        # First group regions by vocab
        grouped: dict = {}
        if regions:
            for region in regions:
                vocab = region.vocabulary or "1"
                if vocab in self.region_vocabularies or not self.region_vocabularies:
                    if vocab not in grouped:
                        grouped[vocab] = {
                            "regions": [],
                        }
                    grouped[vocab]["regions"].append(copy.deepcopy(region))
        elif countries:
            # Add a section for default region, so countries are added to it
            # If we don't do this the countries will be lost
            grouped["1"] = {
                "regions": [],
            }

        # Now for each vocabulary we need to add the countries
        for vocab, data in grouped.items():
            data["countries"] = [copy.deepcopy(country) for country in countries]

        # Now normalise percentages within each vocab group
        for vocab, data in grouped.items():
            total = sum(r.percentage or 0 for r in data["regions"]) + sum(
                c.percentage or 0 for c in data["countries"]
            )
            if total > 0:  # we only normalise if we have valid percentages
                for region in data["regions"]:
                    if region.percentage:
                        region.percentage = (region.percentage / total) * 100
                for country in data["countries"]:
                    if country.percentage:
                        country.percentage = (country.percentage / total) * 100

        return grouped
