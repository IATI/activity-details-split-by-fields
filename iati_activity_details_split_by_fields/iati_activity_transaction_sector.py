from typing import Optional

from .iati_activity_sector import IATIActivitySector


class IATIActivityTransactionSector:

    def __init__(
        self,
        vocabulary=None,
        code=None,
        iati_activity_sector: Optional[IATIActivitySector] = None,
    ):
        self.vocabulary = vocabulary
        self.code = code
        if iati_activity_sector:
            self.vocabulary = iati_activity_sector.vocabulary
            self.code = iati_activity_sector.code

    def get_as_json(self):
        return {
            "vocabulary": self.vocabulary,
            "code": self.code,
        }
