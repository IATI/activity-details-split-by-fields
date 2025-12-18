class IATIActivityRecipientCountry:

    def __init__(self, code=None, percentage=None):
        self.code = code
        self.percentage = percentage

    def get_as_json(self):
        return {
            "code": self.code,
            "percent": self.percentage,
        }
