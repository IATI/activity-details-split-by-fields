class IATIActivityTransactionRecipientRegion:

    def __init__(
        self,
        vocabulary=None,
        code=None,
        iati_activity_recipient_region=None,
    ):
        self.code = code
        self.vocabulary = vocabulary or "1"
        if iati_activity_recipient_region:
            self.code = iati_activity_recipient_region.code
            self.vocabulary = iati_activity_recipient_region.vocabulary

    def get_as_json(self):
        return {
            "vocabulary": self.vocabulary,
            "code": self.code,
        }
