from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_handler.callback_type import CallbackType
from localization.localization import Localization


class SingleApplicationMenu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def create(self):
        markup = InlineKeyboardMarkup([])
        to_main_button = InlineKeyboardButton('<<  ' + self.localization.lang['to_main_menu'],
                                              callback_data=CallbackType.SINGLE_APPLICATION_TO_MAIN)
        back_button = InlineKeyboardButton('<<  ' + self.localization.lang['to_applications_list'],
                                           callback_data=CallbackType.SINGLE_APPLICATION_BACK)
        markup.add(back_button, to_main_button, row_width=1)
        return markup
