from db.constant.application_status import ApplicationStatus
from db.constant.application_type import ApplicationType
from localization.localization import Localization


class DynamicLocalization:

    _mapping = dict()

    def __init__(self, localization: Localization) -> None:
        self.localization = localization
        self._init_mapping()

    def get_text(self, input_text: str) -> str:
        return self._mapping[input_text]

    def _init_mapping(self):
        self._mapping[ApplicationStatus.PENDING] = self.localization.lang['pending']
        self._mapping[ApplicationStatus.APPROVED] = self.localization.lang['approved']
        self._mapping[ApplicationStatus.REJECTED] = self.localization.lang['rejected']

        self._mapping[ApplicationType.TAXI] = self.localization.lang['taxi']
