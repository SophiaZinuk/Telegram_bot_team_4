from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_handler.callback_type import CallbackType
from db.model.model import Application
from localization.dynamic_localization import DynamicLocalization
from localization.localization import Localization


class AdminApplicationsPaginationMenu:

    def __init__(self, localization: Localization, dynamic_localization: DynamicLocalization) -> None:
        self.localization = localization
        self.dynamic_localization = dynamic_localization

    def create(self, applications: List[Application], page: int):
        markup = InlineKeyboardMarkup([])
        backward_button: InlineKeyboardButton = InlineKeyboardButton(
            '<<',
            callback_data=CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACKWARD)
        forward_button = InlineKeyboardButton(
            '>>',
            callback_data=CallbackType.ADMIN_APPLICATIONS_PAGINATION_FORWARD)
        back_button = InlineKeyboardButton(
            self.localization.lang['to_main_menu'],
            callback_data=CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACK)
        for app in applications:
            button_text: str = self._assemble_button_text(app)
            callback_data: str = CallbackType.ADMIN_APPLICATION_PAGINATION_APP + '_' + str(app.id)
            markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))

        if page == 0 and len(applications) == 0:
            markup.add(back_button)
            return markup
        if page == 0 and len(applications) > 0:
            markup.add(forward_button, back_button, row_width=1)
            return markup
        if page > 0 and len(applications) == 0:
            markup.add(backward_button, back_button, row_width=1)
            return markup
        markup.add(backward_button, forward_button, back_button, row_width=2)
        return markup

    def _assemble_button_text(self, app: Application) -> str:
        result: str = ''
        status: str = self.dynamic_localization.get_text(app.application_status)
        app_type: str = self.dynamic_localization.get_text(app.application_type)
        result += '№' + str(app.id) + ': '
        result += self.localization.lang['type'] + ': ' + app_type + '. '
        result += self.localization.lang['status'] + ': ' + status + '.'
        return result

