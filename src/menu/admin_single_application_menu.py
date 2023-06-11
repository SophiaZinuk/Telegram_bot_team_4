from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_handler.callback_type import CallbackType
from localization.localization import Localization


class AdminSingleApplicationMenu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def create(self, operational_buttons_shown: bool):
        markup = InlineKeyboardMarkup([])
        approve_button: InlineKeyboardButton = InlineKeyboardButton(
            text=self.localization.lang['approve'],
            callback_data=CallbackType.ADMIN_SINGLE_APPLICATION_APPROVE)
        reject_button: InlineKeyboardButton = InlineKeyboardButton(
            text=self.localization.lang['reject'],
            callback_data=CallbackType.ADMIN_SINGLE_APPLICATION_REJECT)
        back_button: InlineKeyboardButton = InlineKeyboardButton(
            '<<  ' + self.localization.lang['to_applications_list'],
            callback_data=CallbackType.ADMIN_SINGLE_APPLICATION_BACK)
        main_menu_button: InlineKeyboardButton = InlineKeyboardButton(
            '<<  ' + self.localization.lang['to_main_menu'],
            callback_data=CallbackType.ADMIN_SINGLE_APPLICATION_TO_MAIN)
        if operational_buttons_shown:
            markup.add(approve_button, reject_button, row_width=2)
        markup.add(back_button)
        markup.add(main_menu_button)
        return markup
