class IATIActivityTransactionRecipientCountry:

    def __init__(
        self,
        code=None,
        iati_activity_recipient_country=None,
    ):
        self.code = code
        if iati_activity_recipient_country:
            self.code = iati_activity_recipient_country.code

    def get_as_json(self):
        return {
            "code": self.code,
        }
