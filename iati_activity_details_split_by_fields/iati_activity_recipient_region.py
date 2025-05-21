class IATIActivityRecipientRegion:

    def __init__(self, vocabulary=None, code=None, percentage=None):
        self.vocabulary = vocabulary or "1"
        self.code = code
        self.percentage = percentage
