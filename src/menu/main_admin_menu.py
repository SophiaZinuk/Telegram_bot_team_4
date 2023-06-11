from telebot import types
from callback_handler.callback_type import CallbackType
from localization.localization import Localization


class MainAdminMenu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def create(self):
        markup = types.InlineKeyboardMarkup([
            [
                types.InlineKeyboardButton(text=self.localization.lang['applications_status'],
                                           callback_data=CallbackType.ADMIN_APPLICATIONS_STATUS),
                types.InlineKeyboardButton(text=self.localization.lang['logout'],
                                           callback_data=CallbackType.LOGOUT)
            ],
        ])

        return markup
