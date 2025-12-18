from .iati_activity_transaction_split import IATIActivityTransactionSplit


def filter_split_transactions_by_vocabulary(
    transactions: list[IATIActivityTransactionSplit],
    recipient_region_vocabulary="1",
    sector_vocabulary="1",
):
    """
    Filter split transactions by vocabulary
    :param transactions: list of transactions
    :param recipient_region_vocabulary: vocabulary for recipient region
    :param sector_vocabulary: vocabulary for sector
    :return: filtered transactions
    """
    filtered_transactions = []
    for transaction in transactions:
        if (
            not transaction.recipient_region
            or transaction.recipient_region.vocabulary == recipient_region_vocabulary
        ) and (
            not transaction.sectors
            or any(
                [i for i in transaction.sectors if i.vocabulary == sector_vocabulary]
            )
        ):
            filtered_transactions.append(transaction)
    return filtered_transactions
