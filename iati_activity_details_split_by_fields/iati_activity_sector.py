class IATIActivitySector:

    def __init__(self, vocabulary=None, code=None, percentage=None):
        self.vocabulary = vocabulary or "1"
        self.code = code
        self.percentage = percentage

    def get_as_json(self):
        return {
            "vocabulary": self.vocabulary,
            "code": self.code,
            "percent": self.percentage,
        }
