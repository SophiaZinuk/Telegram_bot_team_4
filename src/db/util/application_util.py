from db.model.model import Application, ApplicationData, User
from localization.dynamic_localization import DynamicLocalization
from localization.localization import Localization


class ApplicationUtil:

    def __init__(
            self,
            localization: Localization,
            dynamic_localization: DynamicLocalization
    ):
        self.localization = localization
        self.dynamic_localization = dynamic_localization

    def assemble_app_text(self, app: Application) -> str:
        result: str = ''
        app_status: str = self.dynamic_localization.get_text(app.application_status)
        app_type: str = self.dynamic_localization.get_text(app.application_type)
        app_data: ApplicationData = app.application_data
        creator: User = app.creator
        result += self.localization.lang['application_number'] + ': ' + str(app.id) + '\n'
        result += self.localization.lang['type'] + ': ' + app_type + '\n'
        result += self.localization.lang['status'] + ': ' + app_status + '\n'
        result += self.localization.lang['car_number'] + ': ' + app_data.car_number + '\n'
        result += self.localization.lang['user_address'] + ': ' + creator.address + '\n'
        return result
